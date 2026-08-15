# backend/agents/state.py
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from models.schemas import (
    DisasterStatus,
    TelemetryData,
    GISFeature,
    TacticalOrder,
    AlertPayload,
    AgentThought,
    AgentGraphNode
)


class MultiAgentWorkflowState(BaseModel):
    """
    Represents the shared working memory across the multi-agent graph.
    Passed between Commander, Risk, Impact, Planning, and Execution agents.
    """
    step_index: int = 0
    scenario_id: str = "mandi_landslide_2026"
    status: DisasterStatus = DisasterStatus.CRITICAL
    threat_level: str = "RED_ALERT_LEVEL_4"
    
    telemetry: TelemetryData = Field(default_factory=TelemetryData)
    gis_features: List[GISFeature] = Field(default_factory=list)
    orders: List[TacticalOrder] = Field(default_factory=list)
    alerts: List[AlertPayload] = Field(default_factory=list)
    reasoning_logs: List[AgentThought] = Field(default_factory=list)
    agent_graph_nodes: List[AgentGraphNode] = Field(default_factory=list)
    
    # Internal agent scratchpads
    weather_risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    terrain_slope_assessment: Dict[str, Any] = Field(default_factory=dict)
    flood_hydrology_assessment: Dict[str, Any] = Field(default_factory=dict)
    population_impact_assessment: Dict[str, Any] = Field(default_factory=dict)
    infrastructure_impact_assessment: Dict[str, Any] = Field(default_factory=dict)
    rescue_plan: Dict[str, Any] = Field(default_factory=dict)
    logistics_plan: Dict[str, Any] = Field(default_factory=dict)
    communication_payload: Dict[str, Any] = Field(default_factory=dict)
    
    execution_completed: bool = False
