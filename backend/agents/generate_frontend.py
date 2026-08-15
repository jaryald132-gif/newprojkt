# backend/agents/generate_frontend.py
import os
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ASCENDANT AGENTS - Autonomous Multi-Agent Disaster Response System</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <!-- Custom Stylesheet -->
  <link rel="stylesheet" href="style.css">
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <!-- Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
</head>
<body class="dark-theme">
  <!-- Top Background Ambient Glows -->
  <div class="ambient-glow glow-1"></div>
  <div class="ambient-glow glow-2"></div>
  <div class="ambient-glow glow-3"></div>

  <!-- Main Application Wrapper -->
  <div class="app-container">
    
    <!-- HEADER BAR -->
    <header class="app-header">
      <div class="header-brand">
        <div class="brand-logo">
          <i data-lucide="shield-alert" class="logo-icon"></i>
          <div class="logo-pulse"></div>
        </div>
        <div class="brand-text">
          <div class="title-row">
            <h1>ASCENDANT AGENTS</h1>
            <span class="badge-vortex">TEAM VORTEX</span>
            <span class="badge-status-pill red-pulse" id="threat-level-badge">RED ALERT LEVEL 4</span>
          </div>
          <p class="subtitle">Autonomous Multi-Agent Crisis Response &bull; Mandi Valley, Himachal Pradesh (31.7087°N, 76.9320°E)</p>
        </div>
      </div>

      <div class="header-meta">
        <!-- Live Workflow Step Indicator -->
        <div class="phase-indicator">
          <span class="phase-label">INCIDENT PHASE</span>
          <span class="phase-value" id="current-phase-text">MONITORING</span>
          <div class="phase-progress-bar">
            <div class="phase-progress-fill" id="phase-progress" style="width: 10%;"></div>
          </div>
        </div>

        <!-- Connection Status -->
        <div class="connection-status" id="connection-status">
          <span class="status-dot green-pulse" id="status-dot"></span>
          <span class="status-text" id="status-text">CONNECTING WS...</span>
        </div>

        <!-- Live Clock & Audio Toggle -->
        <div class="header-controls">
          <button class="icon-btn" id="audio-toggle-btn" title="Toggle Emergency Siren / Voice Announce Audio">
            <i data-lucide="volume-2" id="audio-icon"></i>
          </button>
          <div class="live-clock">
            <i data-lucide="clock" class="clock-icon"></i>
            <span id="live-time-display">--:--:--</span>
          </div>
        </div>
      </div>
    </header>

    <!-- TACTICAL COMMAND ACTION BAR -->
    <section class="command-toolbar">
      <div class="toolbar-left">
        <button class="cmd-btn btn-primary" id="btn-trigger-all">
          <i data-lucide="zap"></i>
          <span>Run Autonomous Chain</span>
          <div class="btn-shine"></div>
        </button>

        <button class="cmd-btn btn-step" id="btn-trigger-step">
          <i data-lucide="play"></i>
          <span>Next Agent Step (<span id="step-counter-label">Step 0/6</span>)</span>
        </button>

        <button class="cmd-btn btn-secondary" id="btn-reset">
          <i data-lucide="rotate-ccw"></i>
          <span>Reset System</span>
        </button>

        <button class="cmd-btn btn-params" id="btn-open-params">
          <i data-lucide="sliders"></i>
          <span>What-If Simulator</span>
        </button>
      </div>

      <div class="toolbar-right">
        <button class="cmd-btn btn-sos" id="btn-open-sos">
          <i data-lucide="radio"></i>
          <span class="sos-text">🆘 Dispatch Citizen SOS</span>
          <span class="sos-ping"></span>
        </button>
      </div>
    </section>

    <!-- TELEMETRY & SITUATIONAL AWARENESS RIBBON -->
    <section class="telemetry-ribbon">
      <div class="telemetry-card">
        <div class="card-icon blue"><i data-lucide="cloud-rain"></i></div>
        <div class="card-content">
          <span class="card-label">DOPPLER PRECIPITATION</span>
          <div class="card-value-row">
            <span class="card-value" id="tel-rainfall">145.0</span>
            <span class="card-unit">mm/hr</span>
          </div>
          <span class="card-status status-danger" id="tel-rainfall-tag">EXTREME CLOUDBURST</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="card-icon red"><i data-lucide="mountain"></i></div>
        <div class="card-content">
          <span class="card-label">SLOPE STABILITY</span>
          <div class="card-value-row">
            <span class="card-value" id="tel-slope">42.0</span>
            <span class="card-unit">° Incline</span>
          </div>
          <span class="card-status status-danger" id="tel-soil-tag">Soil Saturation 94.5%</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="card-icon cyan"><i data-lucide="waves"></i></div>
        <div class="card-content">
          <span class="card-label">BEAS RIVER LEVEL</span>
          <div class="card-value-row">
            <span class="card-value" id="tel-river">4.20</span>
            <span class="card-unit">m</span>
          </div>
          <span class="card-status status-warning" id="tel-river-tag">+1.20m OVER DANGER</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="card-icon orange"><i data-lucide="users"></i></div>
        <div class="card-content">
          <span class="card-label">POPULATION AT RISK</span>
          <div class="card-value-row">
            <span class="card-value" id="tel-pop">4,500</span>
            <span class="card-unit">Citizens</span>
          </div>
          <div class="evac-mini-bar">
            <div class="evac-mini-fill" id="tel-evac-bar" style="width: 28%;"></div>
          </div>
          <span class="card-subtext"><strong id="tel-evac-count">1,240</strong> Evacuated</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="card-icon indigo"><i data-lucide="shield"></i></div>
        <div class="card-content">
          <span class="card-label">ACTIVE RESPONDERS</span>
          <div class="card-value-row">
            <span class="card-value" id="tel-responders">48</span>
            <span class="card-unit">Units</span>
          </div>
          <span class="card-status status-safe">NDRF 14 + SDRF Alpha</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="card-icon red"><i data-lucide="octagon-alert"></i></div>
        <div class="card-content">
          <span class="card-label">NH-154 ARTERY</span>
          <div class="card-value-row">
            <span class="card-value status-danger-text" id="tel-nh154">BLOCKED</span>
          </div>
          <span class="card-subtext">KM 12.4 Landslide Debris</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="card-icon green"><i data-lucide="route"></i></div>
        <div class="card-content">
          <span class="card-label">SH-23 SAFE BYPASS</span>
          <div class="card-value-row">
            <span class="card-value status-safe-text" id="tel-sh23">ACTIVE</span>
          </div>
          <span class="card-subtext">30 HRTC Convoys Rolling</span>
        </div>
      </div>
    </section>

    <!-- MAIN TWO-COLUMN SPLIT GRID -->
    <main class="main-operations-grid">
      
      <!-- LEFT SECTION: GIS MAP & AGENT TOPOLOGY -->
      <section class="ops-left-section">
        
        <!-- GIS OPERATIONS MAP CARD -->
        <div class="dashboard-panel map-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              <i data-lucide="map-pin" class="panel-icon"></i>
              <h2>TACTICAL GIS OPERATIONS THEATER</h2>
              <span class="pill-tag">MANDI LIVE GEOINT</span>
            </div>
            
            <!-- Map Filter Pills -->
            <div class="map-layer-filters">
              <button class="filter-pill active" data-layer="all">All Layers</button>
              <button class="filter-pill" data-layer="hazard_zone"><span class="dot red"></span>Hazards</button>
              <button class="filter-pill" data-layer="evacuation_route"><span class="dot green"></span>Routes</button>
              <button class="filter-pill" data-layer="responder_unit"><span class="dot indigo"></span>Units</button>
              <button class="filter-pill" data-layer="sensor_node"><span class="dot blue"></span>Sensors</button>
              <button class="filter-pill" data-layer="sos_beacon"><span class="dot orange"></span>SOS</button>
            </div>
          </div>

          <!-- Quick Focus Preset Bar -->
          <div class="map-focus-bar">
            <span class="focus-label"><i data-lucide="crosshair"></i> Camera Quick Focus:</span>
            <button class="focus-btn" data-focus="bhiuli">⛰ Bhiuli 42° Slope</button>
            <button class="focus-btn" data-focus="beas">🌊 Beas River Basin</button>
            <button class="focus-btn" data-focus="nh154">🚧 NH-154 Landslide Cut</button>
            <button class="focus-btn" data-focus="sh23">🛣 SH-23 Evacuation Corridor</button>
            <button class="focus-btn" data-focus="college">🏕 Safe Refuge Camp A</button>
            <button class="focus-btn" data-focus="all">🌐 Full Tactical Scope</button>
          </div>

          <!-- Map Element -->
          <div id="gis-map" class="tactical-map"></div>

          <!-- Map Legend Footer -->
          <div class="map-legend">
            <div class="legend-item"><span class="legend-box red-fill"></span> Severe Landslide Zone (42° Slope)</div>
            <div class="legend-item"><span class="legend-box amber-fill"></span> Flash Flood Inundation Margin</div>
            <div class="legend-item"><span class="legend-box green-fill"></span> Safe Evacuation Centers</div>
            <div class="legend-item"><span class="legend-line green-line"></span> SH-23 Active Convoy Bypass</div>
            <div class="legend-item"><span class="legend-line red-line"></span> NH-154 Blocked Road</div>
            <div class="legend-item"><span class="legend-dot orange-pulse"></span> Active Citizen SOS Beacon</div>
          </div>
        </div>

        <!-- 9-AGENT AUTONOMOUS NEURAL TOPOLOGY -->
        <div class="dashboard-panel agent-grid-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              <i data-lucide="network" class="panel-icon purple"></i>
              <h2>AUTONOMOUS MULTI-AGENT SWARM TOPOLOGY</h2>
              <span class="pill-tag">9 SPECIALIZED AGENTS</span>
            </div>
            <span class="agent-sync-pill"><i data-lucide="refresh-cw" class="spin-icon"></i> LangGraph Event Mesh</span>
          </div>

          <div class="agent-cards-grid" id="agent-cards-grid">
            <!-- Dynamically populated 9 Agent Cards -->
          </div>
        </div>
      </section>

      <!-- RIGHT SECTION: LIVE OPERATIONS FEED & MULTI-TAB HUB -->
      <section class="ops-right-section">
        <div class="dashboard-panel feed-panel">
          
          <!-- Tab Navigation Bar -->
          <div class="tab-navbar">
            <button class="tab-btn active" data-tab="reasoning">
              <i data-lucide="brain-circuit"></i>
              <span>Agent Reasoning</span>
              <span class="tab-badge" id="reasoning-count">0</span>
            </button>
            <button class="tab-btn" data-tab="broadcast">
              <i data-lucide="radio-tower"></i>
              <span>CAP Multilingual Alerts</span>
              <span class="tab-badge pulse-badge" id="alert-count">0</span>
            </button>
            <button class="tab-btn" data-tab="orders">
              <i data-lucide="clipboard-list"></i>
              <span>Tactical Orders</span>
              <span class="tab-badge" id="order-count">0</span>
            </button>
            <button class="tab-btn" data-tab="diagnostics">
              <i data-lucide="activity"></i>
              <span>Diagnostics</span>
            </button>
          </div>

          <!-- TAB 1: AGENT REASONING STREAM (CHAIN OF THOUGHT) -->
          <div class="tab-pane active" id="tab-pane-reasoning">
            <div class="feed-filter-bar">
              <div class="search-input-wrap">
                <i data-lucide="search" class="search-icon"></i>
                <input type="text" id="reasoning-search" placeholder="Search thought stream, actions, parameters...">
              </div>
              <select id="agent-filter-select" class="custom-select">
                <option value="all">All Agents</option>
                <option value="commander">AI Commander</option>
                <option value="weather_risk">Weather Risk Agent</option>
                <option value="terrain_risk">Terrain Risk Agent</option>
                <option value="flood_risk">Flood Risk Agent</option>
                <option value="population_impact">Population Impact Agent</option>
                <option value="infrastructure_impact">Infrastructure Agent</option>
                <option value="rescue_planning">Rescue Planning Agent</option>
                <option value="logistics_planning">Logistics Planning Agent</option>
                <option value="communication_execution">Communication Agent</option>
              </select>
            </div>

            <div class="reasoning-stream" id="reasoning-stream">
              <div class="empty-state">
                <i data-lucide="cpu" class="empty-icon"></i>
                <h3>Autonomous Chain Ready</h3>
                <p>Click <strong>"Run Autonomous Chain"</strong> or <strong>"Next Agent Step"</strong> to initiate the multi-agent cognitive loop.</p>
              </div>
            </div>
          </div>

          <!-- TAB 2: MULTILINGUAL CAP EMERGENCY BROADCAST -->
          <div class="tab-pane" id="tab-pane-broadcast">
            <div class="broadcast-container" id="broadcast-container">
              <!-- Dialect Selection Pills -->
              <div class="dialect-tabs">
                <button class="dialect-btn active" data-lang="english">
                  <span>🇬🇧 English</span>
                  <span class="lang-tag">Institutional / Travellers</span>
                </button>
                <button class="dialect-btn" data-lang="hindi">
                  <span>🇮🇳 हिन्दी (Hindi)</span>
                  <span class="lang-tag">Regional State Official</span>
                </button>
                <button class="dialect-btn" data-lang="pahari">
                  <span>🏔 मंडयाली पहाड़ी (Pahari)</span>
                  <span class="lang-tag">Local Mountain Dialect</span>
                </button>
              </div>

              <!-- Active Broadcast Card -->
              <div class="broadcast-card" id="broadcast-card-content">
                <div class="broadcast-card-header">
                  <div class="alert-type-pill">
                    <i data-lucide="flame"></i>
                    <span id="alert-disaster-type">LANDSLIDE & FLASH FLOOD CAP BROADCAST</span>
                  </div>
                  <span class="alert-time" id="alert-timestamp">Dispatched: --:--:--</span>
                </div>

                <h3 class="alert-headline" id="alert-title">IMMEDIATE EVACUATION ORDER: Mandi Landslide & Flood Crisis</h3>

                <div class="broadcast-message-box">
                  <p class="broadcast-text" id="alert-message-text">
                    No active emergency broadcast dispatched yet. Trigger the scenario to generate multilingual Common Alerting Protocol (CAP) broadcasts.
                  </p>
                </div>

                <!-- Channels & Affected Zones -->
                <div class="alert-details-grid">
                  <div class="alert-detail-item">
                    <span class="detail-label"><i data-lucide="map"></i> Affected Sectors</span>
                    <div class="tag-cloud" id="alert-affected-zones">
                      <span class="tag">Bhiuli Ridge</span>
                      <span class="tag">Victoria Bridge</span>
                      <span class="tag">Pandoh Basin</span>
                    </div>
                  </div>

                  <div class="alert-detail-item">
                    <span class="detail-label"><i data-lucide="radio"></i> Dispatched Transmission Gateways</span>
                    <div class="tag-cloud" id="alert-channels">
                      <span class="tag tag-green">CELL_BROADCAST_GEOFENCE</span>
                      <span class="tag tag-green">SMS_GATEWAY</span>
                      <span class="tag tag-green">LOCAL_FM_AIR_MANDI</span>
                      <span class="tag tag-green">OUTDOOR_SIRENS_WARBLE</span>
                    </div>
                  </div>
                </div>

                <!-- Action Controls -->
                <div class="broadcast-actions">
                  <button class="broadcast-action-btn" id="btn-read-aloud">
                    <i data-lucide="volume-2"></i>
                    <span>Speak Emergency Audio (TTS)</span>
                  </button>
                  <button class="broadcast-action-btn" id="btn-copy-alert">
                    <i data-lucide="copy"></i>
                    <span>Copy CAP XML / Text</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 3: TACTICAL ORDERS & DISPATCH BOARD -->
          <div class="tab-pane" id="tab-pane-orders">
            <div class="orders-stream" id="orders-stream">
              <div class="empty-state">
                <i data-lucide="clipboard-check" class="empty-icon"></i>
                <h3>No Tactical Orders Dispatched</h3>
                <p>Orders issued to NDRF, SDRF, Police, and Relief Cells will be displayed here in real time.</p>
              </div>
            </div>
          </div>

          <!-- TAB 4: SENSOR DIAGNOSTICS & TELEMETRY -->
          <div class="tab-pane" id="tab-pane-diagnostics">
            <div class="diagnostics-view">
              <div class="diag-header">
                <h3>Live Geotechnical & Hydrological Ingestion Matrix</h3>
                <p>Ingested from Doppler Radar Mandi (RR-02), Slope Inclinometer (SI-09), and Beas Acoustic Gauge (RG-04).</p>
              </div>

              <div class="diag-cards-grid">
                <div class="diag-card">
                  <div class="diag-top">
                    <span>Doppler Radar (RR-02)</span>
                    <span class="badge red">PEAK SURGE</span>
                  </div>
                  <div class="diag-val" id="diag-rain-val">145.2 mm/hr</div>
                  <div class="diag-meta">Cloudburst Threshold: > 100 mm/hr &bull; Trend: Critical</div>
                </div>

                <div class="diag-card">
                  <div class="diag-top">
                    <span>Borehole Inclinometer (SI-09)</span>
                    <span class="badge red">SLOPE FAILURE</span>
                  </div>
                  <div class="diag-val" id="diag-slope-val">42.0° / 41 mm/hr</div>
                  <div class="diag-meta">Shear strain accelerating &bull; Saturation: 94.5%</div>
                </div>

                <div class="diag-card">
                  <div class="diag-top">
                    <span>Beas River Hydrology (RG-04)</span>
                    <span class="badge amber">SURCHARGE</span>
                  </div>
                  <div class="diag-val" id="diag-river-val">4.20 m / 84k cusecs</div>
                  <div class="diag-meta">Danger Level: 3.00m &bull; Margin: +1.20m flood height</div>
                </div>

                <div class="diag-card">
                  <div class="diag-top">
                    <span>Citizen Evacuation Rate</span>
                    <span class="badge green">CONVOY ACTIVE</span>
                  </div>
                  <div class="diag-val" id="diag-evac-val">1,240 / 4,500</div>
                  <div class="diag-meta">Rate: 60 evacuees/min via SH-23 High Ridge Corridor</div>
                </div>
              </div>

              <div class="diag-system-box">
                <h4>System Architecture & Agent Coordination</h4>
                <p>ASCENDANT AGENTS uses an asynchronous LangGraph multi-agent loop with specialized role delegation, real-time spatial triangulation, and closed-loop feedback telemetry.</p>
                <div class="tech-stack-pills">
                  <span class="pill">FastAPI 0.110</span>
                  <span class="pill">Python 3.14 AsyncIO</span>
                  <span class="pill">WebSocket Stream</span>
                  <span class="pill">Leaflet Dark GIS</span>
                  <span class="pill">Common Alerting Protocol (CAP)</span>
                  <span class="pill">Pydantic V2</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>
    </main>
  </div>

  <!-- CITIZEN SOS MODAL -->
  <div class="modal-overlay" id="sos-modal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title-row">
          <i data-lucide="alert-triangle" class="modal-icon red"></i>
          <h3>Simulate Citizen Emergency SOS Call</h3>
        </div>
        <button class="modal-close-btn" id="sos-modal-close"><i data-lucide="x"></i></button>
      </div>

      <p class="modal-subtitle">Injects an urgent distress call into the AI Commander's real-time reasoning loop, triggering dynamic resource re-routing and tactical dispatch.</p>

      <form id="sos-form" class="modal-form">
        <div class="form-row">
          <div class="form-group">
            <label for="sos-name">Citizen Full Name</label>
            <input type="text" id="sos-name" required value="Ramesh Kumar">
          </div>
          <div class="form-group">
            <label for="sos-contact">Emergency Contact</label>
            <input type="text" id="sos-contact" required value="+91 98160-77821">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="sos-lat">Latitude</label>
            <input type="number" step="0.0001" id="sos-lat" required value="31.7125">
          </div>
          <div class="form-group">
            <label for="sos-lng">Longitude</label>
            <input type="number" step="0.0001" id="sos-lng" required value="76.9380">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="sos-people">Number of Trapped People: <strong id="sos-people-val">6</strong></label>
            <input type="range" id="sos-people" min="1" max="20" value="6" class="range-slider">
          </div>
          <div class="form-group checkbox-group">
            <label class="custom-checkbox">
              <input type="checkbox" id="sos-medical" checked>
              <span class="checkmark"></span>
              <span>Urgent Medical / Trauma Support Needed</span>
            </label>
          </div>
        </div>

        <div class="form-group">
          <label for="sos-details">Emergency Situation Description</label>
          <textarea id="sos-details" rows="3" required>Water entered ground floor, mud sliding near Victoria Bridge cottage. Need immediate evacuation boat!</textarea>
        </div>

        <div class="modal-actions">
          <button type="button" class="cmd-btn btn-secondary" id="sos-btn-cancel">Cancel</button>
          <button type="submit" class="cmd-btn btn-sos-submit" id="sos-btn-submit">
            <i data-lucide="send"></i>
            <span>Transmit SOS Distress Signal</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- WHAT-IF PARAMETERS MODAL -->
  <div class="modal-overlay" id="params-modal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title-row">
          <i data-lucide="sliders" class="modal-icon blue"></i>
          <h3>Crisis Simulation Parameters (What-If Analysis)</h3>
        </div>
        <button class="modal-close-btn" id="params-modal-close"><i data-lucide="x"></i></button>
      </div>

      <p class="modal-subtitle">Modify environmental parameters to simulate different catastrophic conditions in Mandi Valley.</p>

      <form id="params-form" class="modal-form">
        <div class="form-group">
          <div class="slider-header">
            <label for="param-rain">Precipitation Rate</label>
            <span class="slider-val"><strong id="param-rain-val">145.0</strong> mm/hr</span>
          </div>
          <input type="range" id="param-rain" min="40" max="280" step="5" value="145" class="range-slider">
        </div>

        <div class="form-group">
          <div class="slider-header">
            <label for="param-slope">Mountain Slope Angle</label>
            <span class="slider-val"><strong id="param-slope-val">42.0</strong> °</span>
          </div>
          <input type="range" id="param-slope" min="20" max="65" step="1" value="42" class="range-slider">
        </div>

        <div class="form-group">
          <div class="slider-header">
            <label for="param-river">Beas River Gauge Surcharge</label>
            <span class="slider-val"><strong id="param-river-val">4.20</strong> m</span>
          </div>
          <input type="range" id="param-river" min="1.5" max="7.5" step="0.1" value="4.2" class="range-slider">
        </div>

        <div class="preset-buttons">
          <span class="preset-title">Quick Presets:</span>
          <button type="button" class="preset-btn" data-prain="145" data-pslope="42" data-priver="4.2">🔴 Severe Cloudburst (Default)</button>
          <button type="button" class="preset-btn" data-prain="75" data-pslope="30" data-priver="2.6">🟡 Moderate Advisory</button>
          <button type="button" class="preset-btn" data-prain="220" data-pslope="55" data-priver="6.0">🚨 Catastrophic Deluge</button>
        </div>

        <div class="modal-actions">
          <button type="button" class="cmd-btn btn-secondary" id="params-btn-cancel">Close</button>
          <button type="submit" class="cmd-btn btn-primary" id="params-btn-submit">
            <i data-lucide="play-circle"></i>
            <span>Execute Custom Simulation</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- FLOATING TOAST NOTIFICATION CONTAINER -->
  <div class="toast-container" id="toast-container"></div>

  <!-- Main JavaScript Bundle -->
  <script src="main.js"></script>
</body>
</html>
"""

with open(FRONTEND_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print("Generated frontend/index.html successfully.")
