import duckdb
import requests
import json
import re
import time
from bs4 import BeautifulSoup

class MinerDataCollector:
    def __init__(self, miner_ip, db_path='mining_data.duckdb'):
        self.miner_ip = miner_ip
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
    
    def extract_json_from_response(self, url):
        """Extract JSON from potentially HTML-wrapped response"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Try parsing as pure JSON first
            try:
                return response.json()
            except json.JSONDecodeError:
                pass
            
            # Parse as HTML and extract JSON
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for JSON in various common locations
            for tag in ['pre', 'code', 'script']:
                element = soup.find(tag)
                if element:
                    text = element.get_text()
                    # Try to find JSON pattern
                    json_match = re.search(r'(\{.*\})', text, re.DOTALL)
                    if json_match:
                        try:
                            return json.loads(json_match.group(1))
                        except json.JSONDecodeError:
                            continue
            
            # Last resort: extract everything between first { and last }
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            
            raise ValueError("Could not extract valid JSON from response")
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data from {url}: {e}")
    
    def collect_and_store_data(self):
        """Collect data from miner and store in database"""
        try:
            # Fetch and extract JSON data
            miner_data = self.extract_json_from_response(f'http://{self.miner_ip}/api/system/info')
            
            # Write to temporary file for DuckDB to read
            temp_file = 'temp_miner_data.json'
            with open(temp_file, 'w') as f:
                json.dump(miner_data, f)
            
            # Insert main mining statistics
            self.conn.execute(f"""
                INSERT INTO mining_stats (
                    hostname, mac_address, power, voltage, current, temp, vr_temp,
                    hash_rate, expected_hashrate, frequency, shares_accepted,
                    shares_rejected, uptime_seconds, asic_count, small_core_count,
                    asic_model, stratum_url, stratum_port, stratum_user,
                    version, idf_version, board_version, running_partition,
                    ssid, wifi_status, wifi_rssi, core_voltage, core_voltage_actual,
                    best_diff, best_session_diff, stratum_diff, max_power,
                    nominal_voltage, is_using_fallback_stratum, is_psram_available,
                    free_heap, ap_enabled, overheat_mode, overclock_enabled,
                    display, flip_screen, invert_screen, display_timeout,
                    auto_fan_speed, fan_speed, temp_target, fan_rpm,
                    fallback_stratum_url, fallback_stratum_port, fallback_stratum_user,
                    stats_limit, stats_duration
                )
                SELECT 
                    hostname, macAddr, power, voltage, current, temp, vrTemp,
                    hashRate, expectedHashrate, frequency, sharesAccepted,
                    sharesRejected, uptimeSeconds, asicCount, smallCoreCount,
                    ASICModel, stratumURL, stratumPort, stratumUser,
                    version, idfVersion, boardVersion, runningPartition,
                    ssid, wifiStatus, wifiRSSI, coreVoltage, coreVoltageActual,
                    bestDiff, bestSessionDiff, stratumDiff, maxPower,
                    nominalVoltage, isUsingFallbackStratum, isPSRAMAvailable,
                    freeHeap, apEnabled, overheat_mode, overclockEnabled,
                    display, flipscreen, invertscreen, displayTimeout,
                    autofanspeed, fanspeed, temptarget, fanrpm,
                    fallbackStratumURL, fallbackStratumPort, fallbackStratumUser,
                    statsLimit, statsDuration
                FROM read_json('{temp_file}')
            """)
            
            # Get the ID of the inserted record for share rejection reasons
            result = self.conn.execute("SELECT MAX(id) FROM mining_stats").fetchone()
            mining_stats_id = result[0] if result else None
            
            if mining_stats_id and 'sharesRejectedReasons' in miner_data:
                for reason in miner_data['sharesRejectedReasons']:
                    self.conn.execute("""
                        INSERT INTO share_rejection_reasons (mining_stats_id, message, count)
                        VALUES (?, ?, ?)
                    """, [mining_stats_id, reason['message'], reason['count']])
            
            print(f"Successfully collected data from {self.miner_ip}")
            
        except Exception as e:
            print(f"Error collecting data: {e}")
        finally:
            # Clean up temporary file
            import os
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def run_continuous_collection(self, interval_seconds=300):
        """Run continuous data collection"""
        while True:
            self.collect_and_store_data()
            time.sleep(interval_seconds)

# Usage
if __name__ == "__main__":
    collector = MinerDataCollector('192.168.1.100')  # Replace with your miner IP
    collector.run_continuous_collection(300)  # Collect every 5 minutes
