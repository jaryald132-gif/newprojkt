# backend/main.py
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional

from models.schemas import (
    DisasterState,
    ScenarioTriggerRequest,
    SOSRequest
)
from agents.orchestrator import orchestrator

app = FastAPI(
    title="ASCENDANT AGENTS - Autonomous Multi-Agent Disaster Response System",
    description="Backend API for Team VORTEX Hackathon Prototype - Mandi, Himachal Pradesh Landslide Crisis",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager for live state streaming
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()


@app.get("/")
def read_root():
    return {
        "project": "ASCENDANT AGENTS",
        "team": "Team VORTEX",
        "system": "Autonomous Multi-Agent Disaster Response System",
        "location": "Mandi, Himachal Pradesh, India",
        "scenario": "Severe Cloudburst, 42-Degree°°° Mountain Slope Landslide & Flash Flood",
        "status": "ONLINE",
        "endpoints": {
            "state": "/api/scenario/state",
            "trigger": "/api/scenario/trigger",
            "step": "/api/scenario/step",
            "reset": "/api/scenario/reset",
            "sos": "/api/simulate/sos",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "ascendant-backend",
        "agents_ready": 9
    }


@app.get("/api/scenario/state", response_model=DisasterState)
def get_current_state():
    """
    Returns the current disaster operational state, including telemetry,
    GIS features, tactical orders, alerts, reasoning logs, and graph nodes.
    """
    return orchestrator.get_disaster_state()


@app.post("/api/scenario/trigger", response_model=DisasterState)
async def trigger_mandi_scenario(request: Optional[ScenarioTriggerRequest] = None):
    """
    Executes the complete autonomous multi-agent disaster response chain for Mandi, HP.
    """
    rain = request.rainfall_mm_hr if request and request.rainfall_mm_hr else 145.0
    slope = request.slope_deg if request and request.slope_deg else 42.0
    river = request.river_level_m if request and request.river_level_m else 4.2
    
    state = orchestrator.run_full_scenario(rainfall=rain, slope=slope, river=river)
    await manager.broadcast({"event": "SCENARIO_TRIGGERED", "state": state.model_dump()})
    return state


@app.post("/api/scenario/step", response_model=DisasterState)
async def execute_agent_step():
    """
    Executes one step in the multi-agent graph (for interactive presentation mode).
    """
    state = orchestrator.execute_step()
    await manager.broadcast({"event": "STEP_EXECUTED", "state": state.model_dump()})
    return state


@app.post("/api/scenario/reset", response_model=DisasterState)
async def reset_scenario():
    """
    Resets the scenario back to pre-disaster monitoring state.
    """
    state = orchestrator.reset_state()
    await manager.broadcast({"event": "STATE_RESET", "state": state.model_dump()})
    return state


@app.post("/api/simulate/sos", response_model=DisasterState)
async def simulate_citizen_sos(sos: SOSRequest):
    """
    Simulates a citizen distress call, triggering dynamic tactical re-planning.
    """
    state = orchestrator.handle_citizen_sos(sos.model_dump())
    await manager.broadcast({"event": "SOS_DISPATCHED", "state": state.model_dump()})
    return state


@app.get("/api/agents/graph")
def get_agent_graph():
    """
    Returns the agent network node and link topology for the frontend visualization.
    """
    state = orchestrator.get_disaster_state()
    links = [
        # Commander orchestrates all clusters
        {"source": "commander", "target": "weather_risk", "label": "Directs Radar Ingestion"},
        {"source": "commander", "target": "terrain_risk", "label": "Directs Slope Inclinometer"},
        {"source": "commander", "target": "flood_risk", "label": "Directs Beas Hydrology"},
        {"source": "weather_risk", "target": "population_impact", "label": "Precipitation Footprint"},
        {"source": "terrain_risk", "target": "infrastructure_impact", "label": "Debris Avalanche Path"},
        {"source": "flood_risk", "target": "population_impact", "label": "Inundation Margin"},
        {"source": "population_impact", "target": "commander", "label": "4,500 Citizens Exposed"},
        {"source": "infrastructure_impact", "target": "commander", "label": "NH-154 Cut; SH-23 Open"},
        {"source": "commander", "target": "rescue_planning", "label": "Orders NDRF/SDRF Deployment"},
        {"source": "commander", "target": "logistics_planning", "label": "Orders SH-23 Evacuation"},
        {"source": "rescue_planning", "target": "communication_execution", "label": "Safe Zones & Helplines"},
        {"source": "logistics_planning", "target": "communication_execution", "label": "Evacuation Corridors"},
        {"source": "communication_execution", "target": "commander", "label": "Multilingual Broadcast Complete"}
    ]
    return {
        "nodes": state.agent_graph_nodes,
        "links": links
    }


@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial state on connection
        await websocket.send_json({"event": "INITIAL_STATE", "state": orchestrator.get_disaster_state().model_dump()})
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "TRIGGER":
                state = orchestrator.run_full_scenario()
                await manager.broadcast({"event": "SCENARIO_TRIGGERED", "state": state.model_dump()})
            elif action == "STEP":
                state = orchestrator.execute_step()
                await manager.broadcast({"event": "STEP_EXECUTED", "state": state.model_dump()})
            elif action == "RESET":
                state = orchestrator.reset_state()
                await manager.broadcast({"event": "STATE_RESET", "state": state.model_dump()})
            elif action == "SOS":
                sos_payload = data.get("payload", {})
                state = orchestrator.handle_citizen_sos(sos_payload)
                await manager.broadcast({"event": "SOS_DISPATCHED", "state": state.model_dump()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    # Test boot or direct CLI execution
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
