package main

import (
    "time"
)

// ShareRejectionReason represents individual share rejection statistics
type ShareRejectionReason struct {
    Message string `json:"message"`
    Count   int    `json:"count"`
}

// MinerStats represents the complete telemetry data from a Bitcoin miner
type MinerStats struct {
    // Device identification
    Hostname   string `json:"hostname"`
    MacAddress string `json:"macAddr"`
    
    // Power and electrical metrics
    Power             float64 `json:"power"`
    Voltage           float64 `json:"voltage"`
    Current           float64 `json:"current"`
    MaxPower          int     `json:"maxPower"`
    NominalVoltage    int     `json:"nominalVoltage"`
    CoreVoltage       int     `json:"coreVoltage"`
    CoreVoltageActual int     `json:"coreVoltageActual"`
    
    // Temperature monitoring
    Temperature float64 `json:"temp"`
    VRTemp      int     `json:"vrTemp"`
    TempTarget  int     `json:"temptarget"`
    OverheatMode int    `json:"overheat_mode"`
    
    // Mining performance
    HashRate         float64 `json:"hashRate"`
    ExpectedHashrate int     `json:"expectedHashrate"`
    Frequency        int     `json:"frequency"`
    BestDiff         string  `json:"bestDiff"`
    BestSessionDiff  string  `json:"bestSessionDiff"`
    StratumDiff      int     `json:"stratumDiff"`
    
    // Share statistics
    SharesAccepted         int                    `json:"sharesAccepted"`
    SharesRejected         int                    `json:"sharesRejected"`
    SharesRejectedReasons  []ShareRejectionReason `json:"sharesRejectedReasons"`
    
    // System information
    UptimeSeconds    int    `json:"uptimeSeconds"`
    ASICCount        int    `json:"asicCount"`
    SmallCoreCount   int    `json:"smallCoreCount"`
    ASICModel        string `json:"ASICModel"`
    Version          string `json:"version"`
    IDFVersion       string `json:"idfVersion"`
    BoardVersion     string `json:"boardVersion"`
    RunningPartition string `json:"runningPartition"`
    
    // Network configuration
    SSID                     string `json:"ssid"`
    WiFiStatus               string `json:"wifiStatus"`
    WiFiRSSI                 int    `json:"wifiRSSI"`
    APEnabled                int    `json:"apEnabled"`
    IsUsingFallbackStratum   int    `json:"isUsingFallbackStratum"`
    
    // Stratum pool configuration
    StratumURL              string `json:"stratumURL"`
    FallbackStratumURL      string `json:"fallbackStratumURL"`
    StratumPort             int    `json:"stratumPort"`
    FallbackStratumPort     int    `json:"fallbackStratumPort"`
    StratumUser             string `json:"stratumUser"`
    FallbackStratumUser     string `json:"fallbackStratumUser"`
    
    // System resources
    IsPSRAMAvailable int   `json:"isPSRAMAvailable"`
    FreeHeap         int64 `json:"freeHeap"`
    
    // Hardware configuration
    OverclockEnabled int    `json:"overclockEnabled"`
    Display          string `json:"display"`
    FlipScreen       int    `json:"flipscreen"`
    InvertScreen     int    `json:"invertscreen"`
    DisplayTimeout   int    `json:"displayTimeout"`
    AutoFanSpeed     int    `json:"autofanspeed"`
    FanSpeed         int    `json:"fanspeed"`
    FanRPM           int    `json:"fanrpm"`
    
    // Statistics configuration
    StatsLimit    int `json:"statsLimit"`
    StatsDuration int `json:"statsDuration"`
    
    // Timestamp for when this data was collected (not in original JSON)
    CollectedAt time.Time `json:"collected_at,omitempty"`
}
