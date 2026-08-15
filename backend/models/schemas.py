from enum import Enum
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    COMMANDER = "commander"
    WEATHER_RISK = "weather_risk"
    TERRAIN_RISK = "terrain_risk"
    FLOOD_RISK = "flood_risk"
    POPULATION_IMPACT = "population_impact"
    INFRASTRUCTURE_IMPACT = "infrastructure_impact"
    RESCUE_PLANNING = "rescue_planning"
    LOGISTICS_PLANNING = "logistics_planning"
    COMMUNICATION_EXECUTION = "communication_execution"


class DisasterStatus(str, Enum):
    NORMAL = "NORMAL"
    MONITORING = "MONITORING"
    ADVISORY = "ADVISORY"
    CRITICAL = "CRITICAL"
    RESOLVED = "RESOLVED"


class PriorityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AgentThought(BaseModel):
    id: str
    agent_id: AgentType
    agent_name: str
    agent_role: str
    timestamp: str
    step_index: int
    thought: str
    action_taken: str
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    raw_prompt_preview: Optional[str] = None
    structured_output: Dict[str, Any] = Field(default_factory=dict)


class TelemetryData(BaseModel):
    rainfall_mm_hr: float = 145.0
    slope_angle_deg: float = 42.0
    river_level_m: float = 4.2
    river_danger_level_m: float = 3.0
    soil_moisture_pct: float = 94.5
    population_at_risk: int = 4500
    evacuated_count: int = 0
    active_responders_count: int = 48
    nh154_status: str = "BLOCKED_LANDSLIDE"
    sh23_status: str = "OPEN_EVACUATION_CORRIDOR"
    weather_condition: str = "Severe Cloudburst & Torrential Downpour"
    last_updated: str = "Just now"


class GISFeature(BaseModel):
    id: str
    feature_type: str  # "hazard_zone" | "moderate_zone" | "safe_zone" | "road_block" | "evacuation_route" | "responder_unit" | "sensor_node" | "sos_beacon"
    name: str
    coordinates: Union[List[float], List[List[float]], List[List[List[float]]]]
    properties: Dict[str, Any] = Field(default_factory=dict)


class TacticalOrder(BaseModel):
    id: str
    title: str
    target_agency: str
    priority: PriorityLevel
    action_type: str  # "EVACUATION", "ROAD_CLOSURE", "DISPATCH_RESCUE", "AIRLIFT", "RATION_SUPPLY"
    status: str  # "DISPATCHED", "IN_PROGRESS", "EXECUTED", "PENDING"
    details: str
    timestamp: str
    assigned_units: List[str] = Field(default_factory=list)


class AlertPayload(BaseModel):
    id: str
    title: str
    disaster_type: str = "LANDSLIDE_AND_FLASH_FLOOD"
    english_text: str
    hindi_text: str
    pahari_text: str
    affected_zones: List[str]
    broadcast_channels: List[str] = ["CELL_BROADCAST", "CAP_SMS", "VHF_RADIO", "LOCAL_SIRENS"]
    timestamp: str


class AgentGraphNode(BaseModel):
    id: str
    name: str
    role: str
    status: str  # "idle" | "active" | "completed" | "error"
    category: str  # "orchestrator" | "risk" | "impact" | "planning" | "execution"
    last_message: Optional[str] = None


class DisasterState(BaseModel):
    scenario_name: str = "Mandi Cloudburst & Landslide Crisis"
    location_name: str = "Mandi, Himachal Pradesh, India"
    status: DisasterStatus = DisasterStatus.CRITICAL
    threat_level: str = "RED_ALERT_LEVEL_4"
    current_step: int = 0
    total_steps: int = 6
    telemetry: TelemetryData = Field(default_factory=TelemetryData)
    gis_features: List[GISFeature] = Field(default_factory=list)
    orders: List[TacticalOrder] = Field(default_factory=list)
    alerts: List[AlertPayload] = Field(default_factory=list)
    reasoning_logs: List[AgentThought] = Field(default_factory=list)
    agent_graph_nodes: List[AgentGraphNode] = Field(default_factory=list)
    execution_completed: bool = False


class ScenarioTriggerRequest(BaseModel):
    rainfall_mm_hr: Optional[float] = 145.0
    slope_deg: Optional[float] = 42.0
    river_level_m: Optional[float] = 4.2
    trigger_source: Optional[str] = "EARLY_WARNING_RADAR_MANDI"


class SOSRequest(BaseModel):
    citizen_name: str = "Ramesh Kumar"
    lat: float = 31.7125
    lng: float = 76.9380
    contact: str = "+91 98160-XXXXX"
    people_count: int = 6
    emergency_details: str = "Water entered ground floor, mud sliding near Victoria Bridge cottage."
    medical_needed: bool = True
