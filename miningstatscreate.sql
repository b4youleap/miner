CREATE TABLE mining_stats (
    id BIGINT PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(50) NOT NULL,
    mac_address VARCHAR(17) NOT NULL,
    
    -- Power and electrical metrics
    power DECIMAL(10,6),
    voltage DECIMAL(10,2),
    current DECIMAL(10,3),
    max_power INTEGER,
    nominal_voltage INTEGER,
    core_voltage INTEGER,
    core_voltage_actual INTEGER,
    
    -- Temperature monitoring
    temp DECIMAL(5,3),
    vr_temp INTEGER,
    temp_target INTEGER,
    overheat_mode INTEGER,
    
    -- Mining performance
    hash_rate DECIMAL(15,10),
    expected_hashrate INTEGER,
    frequency INTEGER,
    best_diff VARCHAR(20),
    best_session_diff VARCHAR(20),
    stratum_diff INTEGER,
    
    -- Share statistics
    shares_accepted INTEGER,
    shares_rejected INTEGER,
    
    -- System information
    uptime_seconds INTEGER,
    asic_count INTEGER,
    small_core_count INTEGER,
    asic_model VARCHAR(20),
    version VARCHAR(20),
    idf_version VARCHAR(20),
    board_version VARCHAR(10),
    running_partition VARCHAR(20),
    
    -- Network configuration
    ssid VARCHAR(100),
    wifi_status VARCHAR(50),
    wifi_rssi INTEGER,
    ap_enabled INTEGER,
    is_using_fallback_stratum INTEGER,
    
    -- Stratum pool configuration
    stratum_url VARCHAR(200),
    fallback_stratum_url VARCHAR(200),
    stratum_port INTEGER,
    fallback_stratum_port INTEGER,
    stratum_user VARCHAR(200),
    fallback_stratum_user VARCHAR(200),
    
    -- System resources
    is_psram_available INTEGER,
    free_heap BIGINT,
    
    -- Hardware configuration
    overclock_enabled INTEGER,
    display VARCHAR(50),
    flip_screen INTEGER,
    invert_screen INTEGER,
    display_timeout INTEGER,
    auto_fan_speed INTEGER,
    fan_speed INTEGER,
    fan_rpm INTEGER,
    
    -- Statistics configuration
    stats_limit INTEGER,
    stats_duration INTEGER
);
