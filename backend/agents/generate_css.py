# backend/agents/generate_css.py
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

CSS_CONTENT = """/* ==========================================================================
   ASCENDANT AGENTS - CRISIS OPERATIONS DESIGN SYSTEM
   Theme: High-Tech Tactical Defense / Crisis Command Center (Dark Glassmorphism)
   ========================================================================== */

:root {
  /* Color Palette */
  --bg-base: #060911;
  --bg-surface: #0c111e;
  --bg-surface-elevated: #131b2e;
  --bg-surface-hover: #1a243d;
  --bg-card: rgba(16, 23, 41, 0.75);
  --bg-glass: rgba(12, 17, 30, 0.85);

  --border-subtle: rgba(255, 255, 255, 0.07);
  --border-medium: rgba(255, 255, 255, 0.14);
  --border-focus: #6366f1;

  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-highlight: #ffffff;

  /* Tactical Accents */
  --accent-commander: #8b5cf6;
  --accent-commander-glow: rgba(139, 92, 246, 0.35);
  --accent-danger: #ef4444;
  --accent-danger-glow: rgba(239, 68, 68, 0.35);
  --accent-warning: #f59e0b;
  --accent-warning-glow: rgba(245, 158, 11, 0.3);
  --accent-safe: #10b981;
  --accent-safe-glow: rgba(16, 185, 129, 0.35);
  --accent-cyan: #06b6d4;
  --accent-cyan-glow: rgba(6, 182, 212, 0.3);
  --accent-blue: #3b82f6;

  /* Typography */
  --font-heading: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Shadows & Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 20px;
  --shadow-panel: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  --shadow-glow-red: 0 0 20px rgba(239, 68, 68, 0.4);
  --shadow-glow-purple: 0 0 20px rgba(139, 92, 246, 0.4);
}

/* Reset & Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  background-color: var(--bg-base);
  color: var(--text-primary);
  font-family: var(--font-body);
  overflow-x: hidden;
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* Custom Tactical Scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Ambient Glow Backgrounds */
.ambient-glow {
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(120px);
  z-index: 0;
  opacity: 0.25;
}
.glow-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #ef4444 0%, transparent 70%);
  top: -150px;
  left: 10%;
}
.glow-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #6366f1 0%, transparent 70%);
  top: 30%;
  right: -100px;
}
.glow-3 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #06b6d4 0%, transparent 70%);
  bottom: -100px;
  left: 25%;
}

/* Main Container */
.app-container {
  position: relative;
  z-index: 1;
  max-width: 1720px;
  margin: 0 auto;
  padding: 14px 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 100vh;
}

/* ==========================================================================
   HEADER SECTION
   ========================================================================== */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-lg);
  padding: 12px 20px;
  box-shadow: var(--shadow-panel);
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-logo {
  position: relative;
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #7c3aed, #ef4444);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 16px rgba(239, 68, 68, 0.4);
}

.logo-icon {
  width: 26px;
  height: 26px;
}

.logo-pulse {
  position: absolute;
  inset: -3px;
  border-radius: var(--radius-md);
  border: 2px solid #ef4444;
  opacity: 0.6;
  animation: radar-ping 2.5s infinite;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.title-row h1 {
  font-family: var(--font-heading);
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  background: linear-gradient(to right, #ffffff, #cbd5e1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.badge-vortex {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(139, 92, 246, 0.2);
  color: #c084fc;
  border: 1px solid rgba(139, 92, 246, 0.4);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  letter-spacing: 0.5px;
}

.badge-status-pill {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  letter-spacing: 0.8px;
}

.red-pulse {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.5);
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
  animation: pulse-border-red 2s infinite;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 0.82rem;
  font-weight: 400;
  margin-top: 2px;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 20px;
}

.phase-indicator {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 140px;
}

.phase-label {
  font-size: 0.68rem;
  font-family: var(--font-mono);
  color: var(--text-muted);
  font-weight: 600;
}

.phase-value {
  font-family: var(--font-heading);
  font-size: 0.9rem;
  font-weight: 700;
  color: #a5b4fc;
}

.phase-progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.phase-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #10b981);
  transition: width 0.5s ease;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.35);
  padding: 6px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
  font-size: 0.75rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.green-pulse {
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: var(--text-primary);
}

.live-clock {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 0, 0, 0.35);
  padding: 6px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #94a3b8;
}

.clock-icon {
  width: 14px;
  height: 14px;
  color: var(--accent-cyan);
}

/* ==========================================================================
   COMMAND TOOLBAR
   ========================================================================== */
.command-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.cmd-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  border-radius: var(--radius-md);
  font-family: var(--font-heading);
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid transparent;
  outline: none;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.55);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transform: skewX(-20deg);
  animation: shine 3.5s infinite;
}

.btn-step {
  background: var(--bg-surface-elevated);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.btn-step:hover {
  background: rgba(56, 189, 248, 0.15);
  border-color: #38bdf8;
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--bg-surface);
  color: var(--text-secondary);
  border: 1px solid var(--border-medium);
}

.btn-secondary:hover {
  background: var(--bg-surface-hover);
  color: var(--text-primary);
}

.btn-params {
  background: var(--bg-surface);
  color: #c084fc;
  border: 1px solid rgba(192, 132, 252, 0.25);
}

.btn-params:hover {
  background: rgba(192, 132, 252, 0.15);
}

.btn-sos {
  position: relative;
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  color: white;
  padding: 9px 20px;
  box-shadow: 0 4px 18px rgba(220, 38, 38, 0.45);
  animation: pulse-sos 2s infinite;
}

.btn-sos:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 6px 24px rgba(220, 38, 38, 0.7);
}

.sos-text {
  font-weight: 700;
  letter-spacing: 0.5px;
}

/* ==========================================================================
   TELEMETRY RIBBON
   ========================================================================== */
.telemetry-ribbon {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}

.telemetry-card {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: border-color 0.2s, transform 0.2s;
}

.telemetry-card:hover {
  border-color: var(--border-medium);
  transform: translateY(-1px);
}

.card-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon.blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.card-icon.red { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.card-icon.cyan { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }
.card-icon.orange { background: rgba(249, 115, 22, 0.15); color: #fb923c; }
.card-icon.indigo { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.card-icon.green { background: rgba(16, 185, 129, 0.15); color: #34d399; }

.card-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.card-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--text-muted);
  font-weight: 700;
  letter-spacing: 0.5px;
}

.card-value-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.card-value {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-highlight);
}

.card-unit {
  font-size: 0.72rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.card-status {
  font-size: 0.68rem;
  font-weight: 600;
  border-radius: 4px;
  padding: 1px 6px;
  display: inline-block;
  margin-top: 3px;
  width: fit-content;
}

.status-danger {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.status-warning {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

.status-safe {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.status-danger-text { color: #ef4444; }
.status-safe-text { color: #10b981; }

.card-subtext {
  font-size: 0.68rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.evac-mini-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin: 3px 0 2px;
}

.evac-mini-fill {
  height: 100%;
  background: #10b981;
  transition: width 0.6s ease;
}

/* ==========================================================================
   MAIN TWO-COLUMN OPERATIONS GRID
   ========================================================================== */
.main-operations-grid {
  display: grid;
  grid-template-columns: 58% 42%;
  gap: 14px;
  flex: 1;
}

@media (max-width: 1200px) {
  .main-operations-grid {
    grid-template-columns: 1fr;
  }
}

.ops-left-section, .ops-right-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Dashboard Panel Card */
.dashboard-panel {
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-panel);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(12, 17, 30, 0.6);
  flex-wrap: wrap;
  gap: 10px;
}

.panel-title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-icon {
  width: 18px;
  height: 18px;
  color: #38bdf8;
}
.panel-icon.purple { color: #a855f7; }

.panel-header h2 {
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--text-highlight);
}

.pill-tag {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.07);
  color: #94a3b8;
  padding: 2px 6px;
  border-radius: 4px;
}

.agent-sync-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #c084fc;
}

.spin-icon {
  width: 12px;
  height: 12px;
  animation: spin 6s linear infinite;
}

/* ==========================================================================
   GIS MAP & CONTROLS
   ========================================================================== */
.map-layer-filters {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.filter-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  font-size: 0.72rem;
  padding: 3px 8px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-pill:hover, .filter-pill.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-color: var(--border-medium);
}

.filter-pill .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.dot.red { background: #ef4444; }
.dot.green { background: #10b981; }
.dot.indigo { background: #6366f1; }
.dot.blue { background: #38bdf8; }
.dot.orange { background: #f97316; }

.map-focus-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(6, 9, 17, 0.85);
  border-bottom: 1px solid var(--border-subtle);
  overflow-x: auto;
  white-space: nowrap;
}

.focus-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
  font-weight: 600;
  margin-right: 4px;
}

.focus-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  font-size: 0.72rem;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.focus-btn:hover {
  background: rgba(99, 102, 241, 0.2);
  color: white;
  border-color: rgba(99, 102, 241, 0.4);
}

.tactical-map {
  width: 100%;
  height: 400px;
  background: #0b0f19;
}

/* Custom Leaflet Map Dark Styling */
.leaflet-container {
  background: #0b0f19 !important;
  font-family: var(--font-body);
}

.leaflet-popup-content-wrapper {
  background: rgba(15, 23, 42, 0.95) !important;
  backdrop-filter: blur(12px);
  color: #f8fafc !important;
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-md) !important;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7);
  padding: 2px !important;
}

.leaflet-popup-tip {
  background: rgba(15, 23, 42, 0.95) !important;
}

.custom-popup-box h4 {
  font-family: var(--font-heading);
  font-size: 0.92rem;
  font-weight: 700;
  color: #38bdf8;
  margin-bottom: 4px;
}

.custom-popup-box p {
  font-size: 0.78rem;
  color: #cbd5e1;
  line-height: 1.4;
  margin-bottom: 6px;
}

.custom-popup-box .badge-row {
  display: flex;
  gap: 5px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.custom-popup-box .pop-badge {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.1);
}

.map-legend {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 8px 16px;
  background: rgba(12, 17, 30, 0.8);
  border-top: 1px solid var(--border-subtle);
  font-size: 0.72rem;
  color: var(--text-secondary);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-box {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}
.red-fill { background: rgba(239, 68, 68, 0.5); border: 1px solid #ef4444; }
.amber-fill { background: rgba(245, 158, 11, 0.5); border: 1px solid #f59e0b; }
.green-fill { background: rgba(16, 185, 129, 0.5); border: 1px solid #10b981; }

.legend-line {
  width: 18px;
  height: 3px;
  border-radius: 2px;
}
.green-line { background: #10b981; box-shadow: 0 0 6px #10b981; }
.red-line { background: #ef4444; border-top: 1px dashed #ef4444; }

.legend-dot.orange-pulse {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #f97316;
  box-shadow: 0 0 8px #f97316;
  animation: pulse-sos 1.5s infinite;
}

/* ==========================================================================
   9-AGENT AUTONOMOUS NEURAL TOPOLOGY
   ========================================================================== */
.agent-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 12px 14px;
  background: rgba(8, 12, 22, 0.5);
}

@media (max-width: 900px) {
  .agent-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.agent-node-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.agent-node-card:hover {
  background: var(--bg-surface-elevated);
  border-color: var(--border-medium);
  transform: translateY(-2px);
}

.agent-node-card.active {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.12);
  box-shadow: 0 0 16px rgba(139, 92, 246, 0.3);
}

.agent-node-card.completed {
  border-color: rgba(16, 185, 129, 0.4);
}

.agent-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.agent-avatar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.agent-avatar {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
}

.agent-avatar.orchestrator { background: rgba(139, 92, 246, 0.2); color: #c084fc; }
.agent-avatar.risk { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.agent-avatar.impact { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.agent-avatar.planning { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.agent-avatar.execution { background: rgba(16, 185, 129, 0.2); color: #34d399; }

.agent-name {
  font-family: var(--font-heading);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-highlight);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 110px;
}

.agent-status-badge {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 999px;
  text-transform: uppercase;
}

.agent-status-badge.idle { background: rgba(255, 255, 255, 0.08); color: #94a3b8; }
.agent-status-badge.active {
  background: rgba(139, 92, 246, 0.3);
  color: #d8b4fe;
  border: 1px solid #a855f7;
  animation: pulse-border-purple 1.5s infinite;
}
.agent-status-badge.completed { background: rgba(16, 185, 129, 0.25); color: #6ee7b7; }

.agent-role {
  font-size: 0.68rem;
  color: var(--text-secondary);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.agent-last-msg {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: #38bdf8;
  background: rgba(0, 0, 0, 0.3);
  padding: 4px 6px;
  border-radius: var(--radius-sm);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ==========================================================================
   RIGHT SECTION: TABS & FEEDS
   ========================================================================== */
.feed-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 720px;
}

.tab-navbar {
  display: flex;
  align-items: center;
  background: rgba(8, 12, 22, 0.85);
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 10px;
  overflow-x: auto;
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 12px 16px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  font-family: var(--font-heading);
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tab-btn.active {
  color: #38bdf8;
  border-bottom-color: #38bdf8;
  background: rgba(56, 189, 248, 0.06);
}

.tab-badge {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  background: rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  padding: 1px 6px;
  border-radius: 999px;
}

.pulse-badge {
  background: rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  animation: pulse-sos 2s infinite;
}

.tab-pane {
  display: none;
  flex-direction: column;
  flex: 1;
  padding: 12px 16px;
  overflow-y: auto;
}

.tab-pane.active {
  display: flex;
}

/* Tab 1: Agent Reasoning Stream */
.feed-filter-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.search-input-wrap {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: var(--text-muted);
}

.search-input-wrap input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 7px 10px 7px 32px;
  color: var(--text-primary);
  font-size: 0.78rem;
  outline: none;
}

.search-input-wrap input:focus {
  border-color: var(--border-focus);
}

.custom-select {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  padding: 7px 12px;
  border-radius: var(--radius-md);
  font-size: 0.78rem;
  outline: none;
  cursor: pointer;
}

.reasoning-stream {
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  max-height: 600px;
  padding-right: 4px;
}

.reasoning-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: slide-up 0.3s ease-out;
}

.reasoning-card:hover {
  border-color: var(--border-medium);
}

.thought-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.thought-agent-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.thought-agent-name {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 0.85rem;
  color: #38bdf8;
}

.thought-step-badge {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  padding: 1px 6px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.08);
  color: #94a3b8;
}

.thought-time-conf {
  display: flex;
  align-items: center;
  gap: 8px;
}

.thought-conf {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  padding: 1px 6px;
  border-radius: 4px;
}

.thought-time {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--text-muted);
}

.thought-body {
  font-size: 0.8rem;
  line-height: 1.45;
  color: #e2e8f0;
}

.thought-action-badge {
  background: rgba(16, 185, 129, 0.1);
  border-left: 3px solid #10b981;
  padding: 6px 10px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #a7f3d0;
}

.thought-prompt-preview {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--text-muted);
  background: rgba(0, 0, 0, 0.35);
  padding: 6px 8px;
  border-radius: var(--radius-sm);
}

/* Tab 2: Multilingual CAP Alerts */
.broadcast-container {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.dialect-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.dialect-btn {
  flex: 1;
  min-width: 140px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.dialect-btn:hover {
  background: var(--bg-surface-elevated);
}

.dialect-btn.active {
  background: rgba(99, 102, 241, 0.15);
  border-color: #6366f1;
  color: white;
}

.dialect-btn span {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 0.85rem;
}

.dialect-btn .lang-tag {
  font-size: 0.65rem;
  color: var(--text-muted);
  font-weight: 400;
}

.broadcast-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.broadcast-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.alert-type-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: #f87171;
  background: rgba(239, 68, 68, 0.15);
  padding: 3px 10px;
  border-radius: 999px;
}

.alert-headline {
  font-family: var(--font-heading);
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-highlight);
}

.broadcast-message-box {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  padding: 14px;
}

.broadcast-text {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #f1f5f9;
}

.alert-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.alert-detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--text-muted);
  font-weight: 600;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tag {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  background: rgba(255, 255, 255, 0.07);
  color: #cbd5e1;
  padding: 2px 7px;
  border-radius: 4px;
}

.tag-green {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.broadcast-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
}

.broadcast-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.broadcast-action-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--border-medium);
}

/* Tab 3: Tactical Orders */
.orders-stream {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.order-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: slide-up 0.3s ease-out;
}

.order-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.order-title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.order-title {
  font-family: var(--font-heading);
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-highlight);
}

.order-priority {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
}

.order-priority.CRITICAL { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.5); }
.order-priority.HIGH { background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); }

.order-meta-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.72rem;
  color: var(--text-muted);
}

.order-agency {
  color: #38bdf8;
  font-weight: 600;
}

.order-details {
  font-size: 0.8rem;
  color: #cbd5e1;
  line-height: 1.4;
}

.order-units {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.unit-chip {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  padding: 1px 6px;
  border-radius: 3px;
}

/* Tab 4: Diagnostics */
.diagnostics-view {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.diag-header h3 {
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-highlight);
}

.diag-header p {
  font-size: 0.76rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.diag-cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.diag-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.diag-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-secondary);
}

.diag-top .badge {
  font-size: 0.6rem;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 3px;
}
.badge.red { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.badge.amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.badge.green { background: rgba(16, 185, 129, 0.2); color: #34d399; }

.diag-val {
  font-family: var(--font-heading);
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-highlight);
}

.diag-meta {
  font-size: 0.68rem;
  color: var(--text-muted);
}

.diag-system-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px;
}

.diag-system-box h4 {
  font-family: var(--font-heading);
  font-size: 0.88rem;
  font-weight: 700;
  color: #38bdf8;
  margin-bottom: 4px;
}

.diag-system-box p {
  font-size: 0.78rem;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 10px;
}

.tech-stack-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tech-stack-pills .pill {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  background: rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
  padding: 3px 8px;
  border-radius: 4px;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 20px;
  color: var(--text-muted);
  gap: 10px;
}

.empty-icon {
  width: 44px;
  height: 44px;
  color: #475569;
}

.empty-state h3 {
  font-family: var(--font-heading);
  font-size: 1.05rem;
  color: var(--text-secondary);
}

.empty-state p {
  font-size: 0.8rem;
  max-width: 320px;
  line-height: 1.4;
}

/* ==========================================================================
   MODALS & POPUPS
   ========================================================================== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(4, 7, 14, 0.8);
  backdrop-filter: blur(8px);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-overlay.open {
  display: flex;
  animation: fade-in 0.2s ease-out;
}

.modal-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 540px;
  padding: 22px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  gap: 14px;
  animation: scale-up 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-icon {
  width: 20px;
  height: 20px;
}
.modal-icon.red { color: #ef4444; }
.modal-icon.blue { color: #38bdf8; }

.modal-header h3 {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-highlight);
}

.modal-close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
}

.modal-close-btn:hover {
  color: white;
}

.modal-subtitle {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 10px;
  color: var(--text-primary);
  font-size: 0.82rem;
  outline: none;
  font-family: var(--font-body);
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--border-focus);
}

.range-slider {
  accent-color: #6366f1;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  outline: none;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slider-val {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #38bdf8;
}

.checkbox-group {
  justify-content: center;
}

.custom-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.78rem;
  color: #cbd5e1;
  cursor: pointer;
}

.preset-buttons {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 4px;
}

.preset-title {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--text-muted);
}

.preset-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.76rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s;
}

.preset-btn:hover {
  background: rgba(99, 102, 241, 0.15);
  color: white;
  border-color: rgba(99, 102, 241, 0.4);
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-sos-submit {
  background: linear-gradient(135deg, #dc2626, #991b1b);
  color: white;
}

/* Toast Notifications */
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10000;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  color: white;
  font-size: 0.82rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slide-in 0.3s ease-out;
}

.toast.success { border-left: 4px solid #10b981; }
.toast.danger { border-left: 4px solid #ef4444; }
.toast.info { border-left: 4px solid #38bdf8; }

/* ==========================================================================
   ANIMATIONS & KEYFRAMES
   ========================================================================== */
@keyframes pulse-border-red {
  0%, 100% { box-shadow: 0 0 10px rgba(239, 68, 68, 0.2); }
  50% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }
}

@keyframes pulse-border-purple {
  0%, 100% { box-shadow: 0 0 10px rgba(139, 92, 246, 0.2); }
  50% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.6); }
}

@keyframes pulse-sos {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes radar-ping {
  0% { transform: scale(0.95); opacity: 0.8; }
  100% { transform: scale(1.4); opacity: 0; }
}

@keyframes shine {
  0% { left: -100%; }
  20% { left: 200%; }
  100% { left: 200%; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scale-up {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
"""

with open(FRONTEND_DIR / "style.css", "w", encoding="utf-8") as f:
    f.write(CSS_CONTENT)

print("Generated frontend/style.css successfully.")
