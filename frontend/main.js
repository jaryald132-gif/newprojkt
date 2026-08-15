/**
 * ASCENDANT AGENTS - CRISIS OPERATIONS CENTER
 * Frontend Client Engine (Vortex Real-time Multi-Agent Controller)
 */

// Configuration
const CONFIG = {
  API_BASE: 'http://127.0.0.1:8000',
  WS_URL: 'ws://127.0.0.1:8000/ws/stream',
  MAP_CENTER: [31.7087, 76.9320],
  MAP_DEFAULT_ZOOM: 14,
  POLL_INTERVAL_MS: 3000
};

// Global App State
const state = {
  disasterState: null,
  ws: null,
  wsConnected: false,
  activeLanguage: 'english', // 'english' | 'hindi' | 'pahari'
  activeAgentFilter: 'all',
  activeMapFilter: 'all',
  audioEnabled: true,
  map: null,
  mapLayers: {
    hazards: null,
    routes: null,
    responders: null,
    sensors: null,
    sos: null
  },
  layerItemRefs: []
};

// Agent Category and Icon Mapping
const AGENT_METADATA = {
  commander: { icon: 'shield-alert', category: 'orchestrator', color: '#8b5cf6', badge: 'AI Commander' },
  weather_risk: { icon: 'cloud-rain', category: 'risk', color: '#ef4444', badge: 'Weather Risk' },
  terrain_risk: { icon: 'mountain', category: 'risk', color: '#ef4444', badge: 'Terrain Risk' },
  flood_risk: { icon: 'waves', category: 'risk', color: '#06b6d4', badge: 'Flood Risk' },
  population_impact: { icon: 'users', category: 'impact', color: '#f59e0b', badge: 'Population Impact' },
  infrastructure_impact: { icon: 'construction', category: 'impact', color: '#f59e0b', badge: 'Infrastructure' },
  rescue_planning: { icon: 'life-buoy', category: 'planning', color: '#3b82f6', badge: 'Rescue Planning' },
  logistics_planning: { icon: 'truck', category: 'planning', color: '#10b981', badge: 'Logistics Planning' },
  communication_execution: { icon: 'radio-tower', category: 'execution', color: '#f43f5e', badge: 'Multilingual CAP' }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
  initLucide();
  initClock();
  initMap();
  initTabs();
  initControls();
  initModals();
  initWebSocket();
  fetchInitialState();
});

function initLucide() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// Live Clock
function initClock() {
  const clockEl = document.getElementById('live-time-display');
  function updateTime() {
    const now = new Date();
    if (clockEl) {
      clockEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }
  }
  updateTime();
  setInterval(updateTime, 1000);
}

// ==========================================================================
// GIS MAP INITIALIZATION (LEAFLET DARK)
// ==========================================================================
function initMap() {
  const mapEl = document.getElementById('gis-map');
  if (!mapEl) return;

  state.map = L.map('gis-map', {
    center: CONFIG.MAP_CENTER,
    zoom: CONFIG.MAP_DEFAULT_ZOOM,
    zoomControl: true
  });

  // Dark Matter CartoDB Basemap Tiles
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap contributors',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(state.map);

  // Initialize Layer Groups
  state.mapLayers.hazards = L.layerGroup().addTo(state.map);
  state.mapLayers.routes = L.layerGroup().addTo(state.map);
  state.mapLayers.responders = L.layerGroup().addTo(state.map);
  state.mapLayers.sensors = L.layerGroup().addTo(state.map);
  state.mapLayers.sos = L.layerGroup().addTo(state.map);

  // Focus Button Presets
  const focusPresets = {
    bhiuli: { coords: [31.7170, 76.9410], zoom: 15 },
    beas: { coords: [31.7080, 76.9310], zoom: 15 },
    nh154: { coords: [31.7145, 76.9412], zoom: 16 },
    sh23: { coords: [31.7100, 76.9300], zoom: 14 },
    college: { coords: [31.7035, 76.9320], zoom: 16 },
    all: { coords: CONFIG.MAP_CENTER, zoom: CONFIG.MAP_DEFAULT_ZOOM }
  };

  document.querySelectorAll('.focus-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.focus;
      const config = focusPresets[target];
      if (config && state.map) {
        state.map.flyTo(config.coords, config.zoom, { duration: 1.2 });
      }
    });
  });

  // Layer Filter Pills
  document.querySelectorAll('.filter-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeMapFilter = btn.dataset.layer;
      applyMapFilters();
    });
  });
}

function applyMapFilters() {
  const filter = state.activeMapFilter;
  
  if (filter === 'all') {
    state.map.addLayer(state.mapLayers.hazards);
    state.map.addLayer(state.mapLayers.routes);
    state.map.addLayer(state.mapLayers.responders);
    state.map.addLayer(state.mapLayers.sensors);
    state.map.addLayer(state.mapLayers.sos);
  } else {
    state.map.removeLayer(state.mapLayers.hazards);
    state.map.removeLayer(state.mapLayers.routes);
    state.map.removeLayer(state.mapLayers.responders);
    state.map.removeLayer(state.mapLayers.sensors);
    state.map.removeLayer(state.mapLayers.sos);

    if (filter === 'hazard_zone') state.map.addLayer(state.mapLayers.hazards);
    if (filter === 'evacuation_route') state.map.addLayer(state.mapLayers.routes);
    if (filter === 'responder_unit') state.map.addLayer(state.mapLayers.responders);
    if (filter === 'sensor_node') state.map.addLayer(state.mapLayers.sensors);
    if (filter === 'sos_beacon') state.map.addLayer(state.mapLayers.sos);
  }
}

// Render GIS Features on Map
function renderGISFeatures(features) {
  if (!state.map || !features) return;

  // Clear existing layers
  state.mapLayers.hazards.clearLayers();
  state.mapLayers.routes.clearLayers();
  state.mapLayers.responders.clearLayers();
  state.mapLayers.sensors.clearLayers();
  state.mapLayers.sos.clearLayers();

  features.forEach(feat => {
    const type = feat.feature_type;
    const props = feat.properties || {};
    const coords = feat.coordinates;

    // 1. Polygons (Hazard Zones & Safe Shelters)
    if (type === 'hazard_zone' || type === 'moderate_zone' || type === 'safe_zone') {
      const polygon = L.polygon(coords, {
        color: props.color || '#ef4444',
        fillColor: props.fillColor || props.color || '#ef4444',
        fillOpacity: props.fillOpacity || 0.4,
        weight: 2
      });

      const popupContent = `
        <div class="custom-popup-box">
          <h4>${feat.name}</h4>
          <p>${props.description || ''}</p>
          <div class="badge-row">
            <span class="pop-badge" style="background: ${props.color || '#ef4444'}33; color: ${props.color || '#ef4444'}">${props.severity || 'ZONE'}</span>
            ${props.population_exposed ? `<span class="pop-badge">👥 ${props.population_exposed} Exposed</span>` : ''}
            ${props.capacity ? `<span class="pop-badge">🏕 Cap: ${props.capacity}</span>` : ''}
            ${props.current_occupancy ? `<span class="pop-badge">✅ ${props.current_occupancy} Sheltered</span>` : ''}
          </div>
        </div>
      `;
      polygon.bindPopup(popupContent);
      state.mapLayers.hazards.addLayer(polygon);
    }

    // 2. Routes (Blocked NH-154 vs Safe SH-23 Corridor)
    else if (type === 'evacuation_route' || type === 'hazard_route') {
      const polyline = L.polyline(coords, {
        color: props.color || (type === 'evacuation_route' ? '#10b981' : '#ef4444'),
        weight: props.weight || 5,
        dashArray: props.dashArray || null,
        opacity: 0.9
      });

      const popupContent = `
        <div class="custom-popup-box">
          <h4>${feat.name}</h4>
          <p><strong>Status:</strong> ${props.status || 'Active'}</p>
          ${props.travel_time_est ? `<p>⏱ <strong>Transit:</strong> ${props.travel_time_est}</p>` : ''}
          ${props.patrolled_by ? `<p>🛡 <strong>Escort:</strong> ${props.patrolled_by}</p>` : ''}
        </div>
      `;
      polyline.bindPopup(popupContent);
      state.mapLayers.routes.addLayer(polyline);
    }

    // 3. Responder Units (NDRF / SDRF)
    else if (type === 'responder_unit') {
      const responderIcon = L.divIcon({
        className: 'custom-map-icon responder-pin',
        html: `<div style="background: #6366f1; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #ffffff; box-shadow: 0 0 12px #6366f1; font-weight: 800; font-size: 11px;">SAR</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      const marker = L.marker(coords, { icon: responderIcon });
      marker.bindPopup(`
        <div class="custom-popup-box">
          <h4>🛡 ${feat.name}</h4>
          <p><strong>Agency:</strong> ${props.agency || 'Disaster Force'}</p>
          <p><strong>Strength:</strong> ${props.strength} personnel &bull; <strong>Status:</strong> ${props.status}</p>
          <p><strong>Equipment:</strong> ${props.equipment || 'Specialized SAR Gear'}</p>
          <p><strong>Mission:</strong> ${props.mission || 'Active Search & Rescue'}</p>
        </div>
      `);
      state.mapLayers.responders.addLayer(marker);
    }

    // 4. Sensors (Doppler Radar, Inclinometers, River Gauges)
    else if (type === 'sensor_node') {
      const isRadar = feat.id.includes('radar');
      const isRiver = feat.id.includes('river');
      const bg = isRadar ? '#3b82f6' : (isRiver ? '#06b6d4' : '#ef4444');
      const label = isRadar ? 'RAD' : (isRiver ? 'HYD' : 'GEO');

      const sensorIcon = L.divIcon({
        className: 'custom-map-icon sensor-pin',
        html: `<div style="background: ${bg}; color: white; width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; border: 1.5px solid #ffffff; box-shadow: 0 0 10px ${bg}; font-family: monospace; font-weight: 700; font-size: 10px;">${label}</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const marker = L.marker(coords, { icon: sensorIcon });
      marker.bindPopup(`
        <div class="custom-popup-box">
          <h4>📡 ${feat.name}</h4>
          <p><strong>Type:</strong> ${props.sensor_type}</p>
          <p><strong>Reading:</strong> <span style="color: #38bdf8; font-weight: 700;">${props.reading}</span></p>
          <p><strong>Status:</strong> ${props.status || 'ONLINE'}</p>
        </div>
      `);
      state.mapLayers.sensors.addLayer(marker);
    }

    // 5. Road Block Point (NH-154 Landslide)
    else if (type === 'road_block') {
      const blockIcon = L.divIcon({
        className: 'custom-map-icon roadblock-pin',
        html: `<div style="background: #ef4444; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 0 14px #ef4444; font-weight: 800; font-size: 14px;">⛔</div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15]
      });
      const marker = L.marker(coords, { icon: blockIcon });
      marker.bindPopup(`
        <div class="custom-popup-box">
          <h4>⛔ ${feat.name}</h4>
          <p><strong>Road:</strong> ${props.road_name}</p>
          <p><strong>Debris:</strong> ${props.debris_volume} (${props.blocked_distance})</p>
          <p>${props.action}</p>
        </div>
      `);
      state.mapLayers.hazards.addLayer(marker);
    }

    // 6. Citizen SOS Distress Beacon (Animated Sonar Ring)
    else if (type === 'sos_beacon') {
      const sosIcon = L.divIcon({
        className: 'custom-map-icon sos-pin',
        html: `
          <div style="position: relative; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;">
            <div style="position: absolute; inset: 0; border-radius: 50%; border: 3px solid #f97316; animation: radar-ping 1.5s infinite; opacity: 0.8;"></div>
            <div style="background: #ea580c; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid white; font-size: 13px; font-weight: 800; z-index: 2; box-shadow: 0 0 16px #ea580c;">🆘</div>
          </div>
        `,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
      });

      const marker = L.marker(coords, { icon: sosIcon });
      marker.bindPopup(`
        <div class="custom-popup-box">
          <h4 style="color: #fb923c;">🆘 ${feat.name}</h4>
          <p><strong>Requester:</strong> ${props.requester || 'Citizen in Distress'}</p>
          ${props.people_count ? `<p><strong>Family Count:</strong> ${props.people_count} individuals</p>` : ''}
          <p><strong>Emergency:</strong> ${props.details || props.emergency_note || 'Immediate rescue needed'}</p>
          <p><strong>Assigned Unit:</strong> <span style="color: #34d399; font-weight: 700;">${props.assigned_responder || props.assigned_to || 'SDRF Quick Response'}</span></p>
        </div>
      `);
      state.mapLayers.sos.addLayer(marker);
    }
  });

  applyMapFilters();
}

// ==========================================================================
// TABS & INTERACTION
// ==========================================================================
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const target = btn.dataset.tab;
      const targetPane = document.getElementById(`tab-pane-${target}`);
      if (targetPane) targetPane.classList.add('active');
      initLucide();
    });
  });

  // Dialect Tabs in Broadcast Pane
  const dialectBtns = document.querySelectorAll('.dialect-btn');
  dialectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      dialectBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeLanguage = btn.dataset.lang;
      renderBroadcast(state.disasterState ? state.disasterState.alerts : null);
    });
  });

  // Reasoning Search & Filter
  const searchInput = document.getElementById('reasoning-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      renderReasoningLogs(state.disasterState ? state.disasterState.reasoning_logs : []);
    });
  }

  const agentSelect = document.getElementById('agent-filter-select');
  if (agentSelect) {
    agentSelect.addEventListener('change', () => {
      state.activeAgentFilter = agentSelect.value;
      renderReasoningLogs(state.disasterState ? state.disasterState.reasoning_logs : []);
    });
  }
}

// ==========================================================================
// CONTROLS & EVENT LISTENERS
// ==========================================================================
function initControls() {
  // Trigger Full Scenario
  const btnTrigger = document.getElementById('btn-trigger-all');
  if (btnTrigger) {
    btnTrigger.addEventListener('click', async () => {
      btnTrigger.disabled = true;
      btnTrigger.innerHTML = `<i data-lucide="loader-2" class="spin-icon"></i> <span>Orchestrating Agents...</span>`;
      initLucide();

      try {
        if (state.wsConnected && state.ws) {
          state.ws.send(JSON.stringify({ action: 'TRIGGER' }));
        } else {
          const res = await fetch(`${CONFIG.API_BASE}/api/scenario/trigger`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          const data = await res.json();
          handleStateUpdate(data);
        }
        showToast('Autonomous Multi-Agent Crisis Response Executed Successfully!', 'success');
        triggerConfetti();
      } catch (err) {
        showToast(`Execution Error: ${err.message}`, 'danger');
      } finally {
        btnTrigger.disabled = false;
        btnTrigger.innerHTML = `<i data-lucide="zap"></i> <span>Run Autonomous Chain</span> <div class="btn-shine"></div>`;
        initLucide();
      }
    });
  }

  // Step-by-Step Execution
  const btnStep = document.getElementById('btn-trigger-step');
  if (btnStep) {
    btnStep.addEventListener('click', async () => {
      btnStep.disabled = true;
      try {
        if (state.wsConnected && state.ws) {
          state.ws.send(JSON.stringify({ action: 'STEP' }));
        } else {
          const res = await fetch(`${CONFIG.API_BASE}/api/scenario/step`, { method: 'POST' });
          const data = await res.json();
          handleStateUpdate(data);
        }
        showToast('Multi-Agent Step Executed', 'info');
      } catch (err) {
        showToast(`Step Error: ${err.message}`, 'danger');
      } finally {
        btnStep.disabled = false;
      }
    });
  }

  // Reset System
  const btnReset = document.getElementById('btn-reset');
  if (btnReset) {
    btnReset.addEventListener('click', async () => {
      try {
        if (state.wsConnected && state.ws) {
          state.ws.send(JSON.stringify({ action: 'RESET' }));
        } else {
          const res = await fetch(`${CONFIG.API_BASE}/api/scenario/reset`, { method: 'POST' });
          const data = await res.json();
          handleStateUpdate(data);
        }
        showToast('Scenario Reset to Monitoring Baseline', 'info');
      } catch (err) {
        showToast(`Reset Error: ${err.message}`, 'danger');
      }
    });
  }

  // Audio Announce Button
  const btnReadAloud = document.getElementById('btn-read-aloud');
  if (btnReadAloud) {
    btnReadAloud.addEventListener('click', () => {
      playEmergencyAudio();
    });
  }

  // Copy Alert Text
  const btnCopyAlert = document.getElementById('btn-copy-alert');
  if (btnCopyAlert) {
    btnCopyAlert.addEventListener('click', () => {
      const msg = document.getElementById('alert-message-text')?.textContent || '';
      navigator.clipboard.writeText(msg).then(() => {
        showToast('Emergency CAP Text Copied to Clipboard!', 'success');
      });
    });
  }

  // Audio Toggle Header Button
  const audioToggleBtn = document.getElementById('audio-toggle-btn');
  if (audioToggleBtn) {
    audioToggleBtn.addEventListener('click', () => {
      state.audioEnabled = !state.audioEnabled;
      const icon = document.getElementById('audio-icon');
      if (icon) {
        icon.setAttribute('data-lucide', state.audioEnabled ? 'volume-2' : 'volume-x');
        initLucide();
      }
      showToast(`Audio announcements ${state.audioEnabled ? 'Enabled' : 'Muted'}`, 'info');
    });
  }
}

// ==========================================================================
// MODALS LOGIC
// ==========================================================================
function initModals() {
  // SOS Modal
  const sosModal = document.getElementById('sos-modal');
  const btnOpenSos = document.getElementById('btn-open-sos');
  const btnCloseSos = document.getElementById('sos-modal-close');
  const btnCancelSos = document.getElementById('sos-btn-cancel');
  const sosForm = document.getElementById('sos-form');
  const sosPeopleSlider = document.getElementById('sos-people');
  const sosPeopleVal = document.getElementById('sos-people-val');

  if (sosPeopleSlider && sosPeopleVal) {
    sosPeopleSlider.addEventListener('input', (e) => {
      sosPeopleVal.textContent = e.target.value;
    });
  }

  if (btnOpenSos && sosModal) {
    btnOpenSos.addEventListener('click', () => sosModal.classList.add('open'));
  }
  if (btnCloseSos && sosModal) {
    btnCloseSos.addEventListener('click', () => sosModal.classList.remove('open'));
  }
  if (btnCancelSos && sosModal) {
    btnCancelSos.addEventListener('click', () => sosModal.classList.remove('open'));
  }

  if (sosForm) {
    sosForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        citizen_name: document.getElementById('sos-name').value,
        contact: document.getElementById('sos-contact').value,
        lat: parseFloat(document.getElementById('sos-lat').value),
        lng: parseFloat(document.getElementById('sos-lng').value),
        people_count: parseInt(document.getElementById('sos-people').value, 10),
        medical_needed: document.getElementById('sos-medical').checked,
        emergency_details: document.getElementById('sos-details').value
      };

      try {
        if (state.wsConnected && state.ws) {
          state.ws.send(JSON.stringify({ action: 'SOS', payload }));
        } else {
          const res = await fetch(`${CONFIG.API_BASE}/api/simulate/sos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const data = await res.json();
          handleStateUpdate(data);
        }

        sosModal.classList.remove('open');
        showToast(`🚨 Priority SOS Dispatched for ${payload.citizen_name}! AI Commander rerouting SDRF.`, 'danger');

        // Zoom map to SOS location
        if (state.map) {
          state.map.flyTo([payload.lat, payload.lng], 16, { duration: 1.5 });
        }
      } catch (err) {
        showToast(`SOS Error: ${err.message}`, 'danger');
      }
    });
  }

  // What-If Parameters Modal
  const paramsModal = document.getElementById('params-modal');
  const btnOpenParams = document.getElementById('btn-open-params');
  const btnCloseParams = document.getElementById('params-modal-close');
  const btnCancelParams = document.getElementById('params-btn-cancel');
  const paramsForm = document.getElementById('params-form');

  const pRain = document.getElementById('param-rain');
  const pRainVal = document.getElementById('param-rain-val');
  const pSlope = document.getElementById('param-slope');
  const pSlopeVal = document.getElementById('param-slope-val');
  const pRiver = document.getElementById('param-river');
  const pRiverVal = document.getElementById('param-river-val');

  if (pRain && pRainVal) pRain.addEventListener('input', e => pRainVal.textContent = parseFloat(e.target.value).toFixed(1));
  if (pSlope && pSlopeVal) pSlope.addEventListener('input', e => pSlopeVal.textContent = parseFloat(e.target.value).toFixed(1));
  if (pRiver && pRiverVal) pRiver.addEventListener('input', e => pRiverVal.textContent = parseFloat(e.target.value).toFixed(2));

  // Presets
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (pRain) { pRain.value = btn.dataset.prain; pRainVal.textContent = btn.dataset.prain; }
      if (pSlope) { pSlope.value = btn.dataset.pslope; pSlopeVal.textContent = btn.dataset.pslope; }
      if (pRiver) { pRiver.value = btn.dataset.priver; pRiverVal.textContent = btn.dataset.priver; }
    });
  });

  if (btnOpenParams && paramsModal) {
    btnOpenParams.addEventListener('click', () => paramsModal.classList.add('open'));
  }
  if (btnCloseParams && paramsModal) {
    btnCloseParams.addEventListener('click', () => paramsModal.classList.remove('open'));
  }
  if (btnCancelParams && paramsModal) {
    btnCancelParams.addEventListener('click', () => paramsModal.classList.remove('open'));
  }

  if (paramsForm) {
    paramsForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const customPayload = {
        rainfall_mm_hr: parseFloat(pRain.value),
        slope_deg: parseFloat(pSlope.value),
        river_level_m: parseFloat(pRiver.value)
      };

      try {
        const res = await fetch(`${CONFIG.API_BASE}/api/scenario/trigger`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(customPayload)
        });
        const data = await res.json();
        handleStateUpdate(data);
        paramsModal.classList.remove('open');
        showToast('Custom What-If Scenario Triggered Successfully!', 'success');
      } catch (err) {
        showToast(`Simulation Error: ${err.message}`, 'danger');
      }
    });
  }
}

// ==========================================================================
// WEBSOCKET & REST STREAMING
// ==========================================================================
function initWebSocket() {
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');

  try {
    state.ws = new WebSocket(CONFIG.WS_URL);

    state.ws.onopen = () => {
      state.wsConnected = true;
      if (statusDot) {
        statusDot.className = 'status-dot green-pulse';
      }
      if (statusText) {
        statusText.textContent = 'WS STREAM LIVE';
      }
      showToast('Connected to Live Disaster Event Mesh', 'success');
    };

    state.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.state) {
          handleStateUpdate(data.state);
        }
      } catch (err) {
        console.error('Error parsing WS message', err);
      }
    };

    state.ws.onerror = (err) => {
      console.warn('WS error, falling back to REST', err);
      setConnectionFallback();
    };

    state.ws.onclose = () => {
      state.wsConnected = false;
      setConnectionFallback();
      // Retry in 5 seconds
      setTimeout(initWebSocket, 5000);
    };
  } catch (err) {
    console.warn('WebSocket init failure, using REST', err);
    setConnectionFallback();
  }
}

function setConnectionFallback() {
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');
  if (statusDot) statusDot.className = 'status-dot';
  if (statusText) statusText.textContent = 'REST SYNC MODE';
}

async function fetchInitialState() {
  try {
    const res = await fetch(`${CONFIG.API_BASE}/api/scenario/state`);
    if (res.ok) {
      const data = await res.json();
      handleStateUpdate(data);
    }
  } catch (err) {
    console.error('Initial state fetch error:', err);
  }
}

// Central State Dispatcher
function handleStateUpdate(disasterState) {
  if (!disasterState) return;
  state.disasterState = disasterState;

  renderHeader(disasterState);
  renderTelemetry(disasterState.telemetry);
  renderGISFeatures(disasterState.gis_features);
  renderAgentGrid(disasterState.agent_graph_nodes);
  renderReasoningLogs(disasterState.reasoning_logs);
  renderBroadcast(disasterState.alerts);
  renderOrders(disasterState.orders);
  renderDiagnostics(disasterState.telemetry);
  initLucide();
}

// ==========================================================================
// UI RENDERERS
// ==========================================================================
function renderHeader(dState) {
  const threatBadge = document.getElementById('threat-level-badge');
  if (threatBadge) {
    threatBadge.textContent = dState.threat_level ? dState.threat_level.replace(/_/g, ' ') : 'MONITORING';
    threatBadge.className = `badge-status-pill ${dState.status === 'CRITICAL' ? 'red-pulse' : 'green-pulse'}`;
  }

  const phaseText = document.getElementById('current-phase-text');
  const phaseBar = document.getElementById('phase-progress');
  const stepLabel = document.getElementById('step-counter-label');

  const step = dState.current_step || 0;
  const total = dState.total_steps || 6;
  const pct = Math.min(100, Math.round((step / total) * 100));

  const phaseNames = [
    'MONITORING (Standby)',
    'PHASE 1: Risk Assessment',
    'PHASE 2: Impact Analysis',
    'PHASE 3: Tactical Planning',
    'PHASE 4: CAP Alert Broadcast',
    'PHASE 5: Operational Audit',
    'PHASE 6: Stabilized Closed-Loop'
  ];

  if (phaseText) phaseText.textContent = phaseNames[step] || `STEP ${step}/${total}`;
  if (phaseBar) phaseBar.style.width = `${Math.max(10, pct)}%`;
  if (stepLabel) stepLabel.textContent = `Step ${step}/${total}`;
}

function renderTelemetry(tel) {
  if (!tel) return;

  const rEl = document.getElementById('tel-rainfall');
  const sEl = document.getElementById('tel-slope');
  const rivEl = document.getElementById('tel-river');
  const popEl = document.getElementById('tel-pop');
  const evacBar = document.getElementById('tel-evac-bar');
  const evacCount = document.getElementById('tel-evac-count');
  const respEl = document.getElementById('tel-responders');
  const nhEl = document.getElementById('tel-nh154');
  const shEl = document.getElementById('tel-sh23');

  if (rEl) rEl.textContent = tel.rainfall_mm_hr.toFixed(1);
  if (sEl) sEl.textContent = tel.slope_angle_deg.toFixed(1);
  if (rivEl) rivEl.textContent = tel.river_level_m.toFixed(2);
  if (popEl) popEl.textContent = tel.population_at_risk.toLocaleString();
  if (respEl) respEl.textContent = tel.active_responders_count;

  if (evacCount) evacCount.textContent = tel.evacuated_count.toLocaleString();
  if (evacBar && tel.population_at_risk > 0) {
    const evacPct = Math.round((tel.evacuated_count / tel.population_at_risk) * 100);
    evacBar.style.width = `${evacPct}%`;
  }

  if (nhEl) {
    nhEl.textContent = tel.nh154_status.includes('BLOCKED') ? 'BLOCKED' : 'OPEN';
    nhEl.className = tel.nh154_status.includes('BLOCKED') ? 'card-value status-danger-text' : 'card-value status-safe-text';
  }

  if (shEl) {
    shEl.textContent = tel.sh23_status.includes('ACTIVE') || tel.sh23_status.includes('OPEN') ? 'ACTIVE' : 'STANDBY';
    shEl.className = 'card-value status-safe-text';
  }
}

function renderAgentGrid(nodes) {
  const container = document.getElementById('agent-cards-grid');
  if (!container) return;

  if (!nodes || nodes.length === 0) {
    // Default 9 agents if empty
    nodes = Object.keys(AGENT_METADATA).map(id => ({
      id,
      name: AGENT_METADATA[id].badge,
      role: 'Specialized Multi-Agent Node',
      status: 'idle',
      last_message: 'Standby for triggers'
    }));
  }

  container.innerHTML = nodes.map(node => {
    const meta = AGENT_METADATA[node.id] || { icon: 'cpu', category: 'risk', color: '#6366f1', badge: node.name };
    const statusClass = node.status || 'idle';

    return `
      <div class="agent-node-card ${statusClass}" data-agent-id="${node.id}">
        <div class="agent-card-top">
          <div class="agent-avatar-wrap">
            <div class="agent-avatar ${meta.category}">
              <i data-lucide="${meta.icon}"></i>
            </div>
            <span class="agent-name" title="${node.name}">${node.name}</span>
          </div>
          <span class="agent-status-badge ${statusClass}">${statusClass}</span>
        </div>
        <p class="agent-role">${node.role}</p>
        <div class="agent-last-msg" title="${node.last_message || ''}">
          💬 ${node.last_message || 'Listening to event bus...'}
        </div>
      </div>
    `;
  }).join('');

  // Add click listener to filter reasoning stream
  container.querySelectorAll('.agent-node-card').forEach(card => {
    card.addEventListener('click', () => {
      const agentId = card.dataset.agentId;
      const select = document.getElementById('agent-filter-select');
      if (select) {
        select.value = agentId;
        state.activeAgentFilter = agentId;
        renderReasoningLogs(state.disasterState ? state.disasterState.reasoning_logs : []);
        // Switch to reasoning tab
        const reasoningTabBtn = document.querySelector('[data-tab="reasoning"]');
        if (reasoningTabBtn) reasoningTabBtn.click();
      }
    });
  });
}

function renderReasoningLogs(logs) {
  const container = document.getElementById('reasoning-stream');
  const countBadge = document.getElementById('reasoning-count');
  if (!container) return;

  if (countBadge) countBadge.textContent = logs ? logs.length : 0;

  if (!logs || logs.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i data-lucide="cpu" class="empty-icon"></i>
        <h3>Autonomous Chain Ready</h3>
        <p>Click <strong>"Run Autonomous Chain"</strong> or <strong>"Next Agent Step"</strong> to initiate the multi-agent cognitive loop.</p>
      </div>
    `;
    return;
  }

  // Filter logs by agent and search text
  const searchVal = (document.getElementById('reasoning-search')?.value || '').toLowerCase();
  const agentFilter = state.activeAgentFilter;

  const filteredLogs = logs.filter(log => {
    const matchesAgent = agentFilter === 'all' || log.agent_id === agentFilter;
    const matchesSearch = !searchVal ||
      (log.thought && log.thought.toLowerCase().includes(searchVal)) ||
      (log.action_taken && log.action_taken.toLowerCase().includes(searchVal)) ||
      (log.agent_name && log.agent_name.toLowerCase().includes(searchVal));
    return matchesAgent && matchesSearch;
  });

  if (filteredLogs.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i data-lucide="filter" class="empty-icon"></i>
        <h3>No matching reasoning logs</h3>
        <p>Try clearing your search query or selecting "All Agents".</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filteredLogs.map(log => {
    const meta = AGENT_METADATA[log.agent_id] || { icon: 'brain', color: '#6366f1' };
    const confPct = Math.round((log.confidence || 0.95) * 100);

    return `
      <div class="reasoning-card">
        <div class="thought-header">
          <div class="thought-agent-info">
            <span class="thought-agent-name" style="color: ${meta.color};">${log.agent_name}</span>
            <span class="thought-step-badge">Step ${log.step_index}</span>
          </div>
          <div class="thought-time-conf">
            <span class="thought-conf">⚡ ${confPct}% Confidence</span>
            <span class="thought-time">${log.timestamp}</span>
          </div>
        </div>

        <p class="thought-body">${formatThoughtText(log.thought)}</p>

        ${log.action_taken ? `
          <div class="thought-action-badge">
            <strong>ACTION:</strong> ${log.action_taken}
          </div>
        ` : ''}

        ${log.raw_prompt_preview ? `
          <details style="cursor: pointer;">
            <summary style="font-size: 0.68rem; color: #94a3b8;">🔍 Inspect Prompt Formulation</summary>
            <div class="thought-prompt-preview">${log.raw_prompt_preview}</div>
          </details>
        ` : ''}
      </div>
    `;
  }).join('');
}

function formatThoughtText(text) {
  if (!text) return '';
  // Highlight keywords nicely
  return text
    .replace(/(CRITICAL|RED_ALERT_LEVEL_4|BLOCKED|MANDATORY EVACUATION|EMERGENCY)/g, '<strong style="color: #f87171;">$1</strong>')
    .replace(/(OPEN|SAFE|DEPLOYED|CONFIRMED|VERIFIED)/g, '<strong style="color: #34d399;">$1</strong>')
    .replace(/(NH-154|SH-23|NDRF|SDRF|Bhiuli|Pandoh)/g, '<span style="color: #38bdf8; font-weight: 600;">$1</span>');
}

function renderBroadcast(alerts) {
  const countBadge = document.getElementById('alert-count');
  if (countBadge) countBadge.textContent = alerts ? alerts.length : 0;

  const headlineEl = document.getElementById('alert-title');
  const msgEl = document.getElementById('alert-message-text');
  const timeEl = document.getElementById('alert-timestamp');
  const zonesEl = document.getElementById('alert-affected-zones');

  if (!alerts || alerts.length === 0) {
    if (headlineEl) headlineEl.textContent = 'STANDBY: No Active Disaster Broadcast';
    if (msgEl) msgEl.textContent = 'Autonomous multi-agent loop has not yet triggered an emergency alert. Run the crisis simulation to generate multilingual CAP broadcasts.';
    if (timeEl) timeEl.textContent = 'Dispatched: --:--:--';
    return;
  }

  const latest = alerts[alerts.length - 1];
  if (headlineEl) headlineEl.textContent = latest.title || 'IMMEDIATE CRISIS ADVISORY';
  if (timeEl) timeEl.textContent = `Dispatched: ${latest.timestamp}`;

  // Select language
  let messageText = latest.english_text;
  if (state.activeLanguage === 'hindi') messageText = latest.hindi_text;
  if (state.activeLanguage === 'pahari') messageText = latest.pahari_text;

  if (msgEl) msgEl.textContent = messageText;

  if (zonesEl && latest.affected_zones) {
    zonesEl.innerHTML = latest.affected_zones.map(z => `<span class="tag">${z}</span>`).join('');
  }
}

function renderOrders(orders) {
  const container = document.getElementById('orders-stream');
  const countBadge = document.getElementById('order-count');
  if (!container) return;

  if (countBadge) countBadge.textContent = orders ? orders.length : 0;

  if (!orders || orders.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i data-lucide="clipboard-check" class="empty-icon"></i>
        <h3>No Tactical Orders Dispatched</h3>
        <p>Orders issued to NDRF, SDRF, Police, and Relief Cells will appear here in real time.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = orders.map(ord => {
    return `
      <div class="order-card">
        <div class="order-card-top">
          <div class="order-title-wrap">
            <span class="order-priority ${ord.priority}">${ord.priority}</span>
            <span class="order-title">${ord.title}</span>
          </div>
          <span class="order-agency">${ord.target_agency}</span>
        </div>

        <p class="order-details">${ord.details}</p>

        <div class="order-meta-row">
          <span>⏱ ${ord.timestamp}</span>
          <span>⚡ Status: <strong style="color: #34d399;">${ord.status}</strong></span>
          ${ord.assigned_units && ord.assigned_units.length > 0 ? `
            <div class="order-units">
              ${ord.assigned_units.map(u => `<span class="unit-chip">${u}</span>`).join('')}
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function renderDiagnostics(tel) {
  if (!tel) return;
  const rainEl = document.getElementById('diag-rain-val');
  const slopeEl = document.getElementById('diag-slope-val');
  const rivEl = document.getElementById('diag-river-val');
  const evacEl = document.getElementById('diag-evac-val');

  if (rainEl) rainEl.textContent = `${tel.rainfall_mm_hr.toFixed(1)} mm/hr`;
  if (slopeEl) slopeEl.textContent = `${tel.slope_angle_deg.toFixed(1)}° / ${tel.soil_moisture_pct}% sat`;
  if (rivEl) rivEl.textContent = `${tel.river_level_m.toFixed(2)} m (+${(tel.river_level_m - tel.river_danger_level_m).toFixed(2)}m surge)`;
  if (evacEl) evacEl.textContent = `${tel.evacuated_count.toLocaleString()} / ${tel.population_at_risk.toLocaleString()}`;
}

// ==========================================================================
// AUDIO SPEECH SYNTHESIS & SIRENS
// ==========================================================================
function playEmergencyAudio() {
  if (!('speechSynthesis' in window)) {
    showToast('Web Speech API not supported on this browser', 'info');
    return;
  }

  const msg = document.getElementById('alert-message-text')?.textContent || '';
  if (!msg) return;

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(msg);
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  if (state.activeLanguage === 'hindi') {
    utterance.lang = 'hi-IN';
  } else {
    utterance.lang = 'en-US';
  }

  window.speechSynthesis.speak(utterance);
  showToast('Playing Emergency CAP Audio Broadcast...', 'info');
}

// ==========================================================================
// TOAST NOTIFICATIONS & CONFETTI
// ==========================================================================
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  let iconName = 'info';
  if (type === 'success') iconName = 'check-circle';
  if (type === 'danger') iconName = 'alert-octagon';

  toast.innerHTML = `<i data-lucide="${iconName}"></i> <span>${message}</span>`;
  container.appendChild(toast);
  initLucide();

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function triggerConfetti() {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });
  }
}
