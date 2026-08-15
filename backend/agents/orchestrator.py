# backend/agents/orchestrator.py
import asyncio
from typing import List, Dict, Any, Optional
from models.schemas import AgentGraphNode, DisasterState, DisasterStatus
from data.mandi_gis import get_initial_gis_features, get_initial_telemetry
from agents.state import MultiAgentWorkflowState
from agents.commander_agent import CommanderAgent
from agents.risk_agents import WeatherRiskAgent, TerrainRiskAgent, FloodRiskAgent
from agents.impact_agents import PopulationImpactAgent, InfrastructureImpactAgent
from agents.planning_agents import RescuePlanningAgent, LogisticsPlanningAgent
from agents.execution_agents import CommunicationAgent


class MultiAgentOrchestrator:
    """
    Coordinates the multi-agent graph execution (LangGraph-style state machine).
    Supports:
    - Full autonomous scenario simulation run
    - Step-by-step interactive inspection (ideal for hackathon presentations)
    - Dynamic citizen SOS injection & replanning
    - State reset
    """
    def __init__(self):
        self.commander = CommanderAgent()
        self.weather_agent = WeatherRiskAgent()
        self.terrain_agent = TerrainRiskAgent()
        self.flood_agent = FloodRiskAgent()
        self.population_agent = PopulationImpactAgent()
        self.infrastructure_agent = InfrastructureImpactAgent()
        self.rescue_agent = RescuePlanningAgent()
        self.logistics_agent = LogisticsPlanningAgent()
        self.communication_agent = CommunicationAgent()
        
        self.state: MultiAgentWorkflowState = self._create_initial_state()

    def _create_initial_state(self) -> MultiAgentWorkflowState:
        telemetry = get_initial_telemetry()
        gis_features = get_initial_gis_features()
        nodes = self._build_graph_nodes("idle")
        
        return MultiAgentWorkflowState(
            step_index=0,
            scenario_id="mandi_landslide_2026",
            status=DisasterStatus.MONITORING,
            threat_level="YELLOW_WATCH",
            telemetry=telemetry,
            gis_features=gis_features,
            orders=[],
            alerts=[],
            reasoning_logs=[],
            agent_graph_nodes=nodes,
            execution_completed=False
        )

    def _build_graph_nodes(self, default_status: str = "idle") -> List[AgentGraphNode]:
        return [
            AgentGraphNode(
                id="commander",
                name="AI Commander",
                role="Strategic Orchestrator & Executive Directives",
                status=default_status,
                category="orchestrator",
                last_message="Standby for sensor anomalies"
            ),
            AgentGraphNode(
                id="weather_risk",
                name="Weather Risk Agent",
                role="Doppler Radar & Cloudburst Ingestion",
                status=default_status,
                category="risk",
                last_message="Monitoring rainfall rate (mm/hr)"
            ),
            AgentGraphNode(
                id="terrain_risk",
                name="Terrain Risk Agent",
                role="Geotechnical Slope Stability & Inclinometers",
                status=default_status,
                category="risk",
                last_message="Tracking 42° slope shear strain"
            ),
            AgentGraphNode(
                id="flood_risk",
                name="Flood Risk Agent",
                role="Beas River Hydrodynamics & Surcharge",
                status=default_status,
                category="risk",
                last_message="Analyzing River Gauge RG-04"
            ),
            AgentGraphNode(
                id="population_impact",
                name="Population Impact Agent",
                role="Cadastral Census & Vulnerability Overlay",
                status=default_status,
                category="impact",
                last_message="Cross-referencing Ward parcels"
            ),
            AgentGraphNode(
                id="infrastructure_impact",
                name="Infrastructure Agent",
                role="Roads, Bridges & Power Grid Status",
                status=default_status,
                category="impact",
                last_message="Evaluating NH-154 & SH-23"
            ),
            AgentGraphNode(
                id="rescue_planning",
                name="Rescue Planning Agent",
                role="SAR Asset Deployment (NDRF / SDRF)",
                status=default_status,
                category="planning",
                last_message="Synthesizing force layout"
            ),
            AgentGraphNode(
                id="logistics_planning",
                name="Logistics Planning Agent",
                role="Evacuation Corridors & Shelter Fleet",
                status=default_status,
                category="planning",
                last_message="Mapping safe transit corridors"
            ),
            AgentGraphNode(
                id="communication_execution",
                name="Communication Agent",
                role="Multilingual CAP Alerts (EN/HI/Pahari)",
                status=default_status,
                category="execution",
                last_message="Preparing geofenced broadcasts"
            )
        ]

    def _update_node_status(self, node_id: str, status: str, message: Optional[str] = None):
        for node in self.state.agent_graph_nodes:
            if node.id == node_id:
                node.status = status
                if message:
                    node.last_message = message

    def reset_state(self) -> DisasterState:
        self.state = self._create_initial_state()
        return self.get_disaster_state()

    def get_disaster_state(self) -> DisasterState:
        return DisasterState(
            scenario_name="Mandi Cloudburst & Landslide Crisis",
            location_name="Mandi, Himachal Pradesh, India",
            status=self.state.status,
            threat_level=self.state.threat_level,
            current_step=self.state.step_index,
            total_steps=6,
            telemetry=self.state.telemetry,
            gis_features=self.state.gis_features,
            orders=self.state.orders,
            alerts=self.state.alerts,
            reasoning_logs=self.state.reasoning_logs,
            agent_graph_nodes=self.state.agent_graph_nodes,
            execution_completed=self.state.execution_completed
        )

    def execute_step(self) -> DisasterState:
        """
        Executes a single step in the multi-agent graph.
        """
        step = self.state.step_index
        
        if step == 0:
            # Step 0: Commander activates response
            self._update_node_status("commander", "active", "Initiating crisis evaluation")
            thought = self.commander.initial_assessment(self.state)
            self.state.reasoning_logs.append(thought)
            self._update_node_status("commander", "completed", "Tasked Risk Detection cluster")
            self.state.step_index = 1
            
        elif step == 1:
            # Step 1: Risk Detection cluster runs in parallel
            self._update_node_status("weather_risk", "active", "Computing precipitation flux")
            t_weather = self.weather_agent.run(self.state)
            self.state.reasoning_logs.append(t_weather)
            self._update_node_status("weather_risk", "completed", "Extreme Cloudburst detected (145mm/hr)")

            self._update_node_status("terrain_risk", "active", "Calculating slope stability")
            t_terrain = self.terrain_agent.run(self.state)
            self.state.reasoning_logs.append(t_terrain)
            self._update_node_status("terrain_risk", "completed", "Critical Landslide threat on 42° slope")

            self._update_node_status("flood_risk", "active", "Measuring Beas river surge")
            t_flood = self.flood_agent.run(self.state)
            self.state.reasoning_logs.append(t_flood)
            self._update_node_status("flood_risk", "completed", "Beas River +1.2m above danger mark")
            
            self.state.step_index = 2
            
        elif step == 2:
            # Step 2: Impact Assessment cluster runs
            self._update_node_status("population_impact", "active", "Intersecting population parcels")
            t_pop = self.population_agent.run(self.state)
            self.state.reasoning_logs.append(t_pop)
            self._update_node_status("population_impact", "completed", "4,500 people identified at risk")

            self._update_node_status("infrastructure_impact", "active", "Analyzing highway & bridges")
            t_infra = self.infrastructure_agent.run(self.state)
            self.state.reasoning_logs.append(t_infra)
            self._update_node_status("infrastructure_impact", "completed", "NH-154 blocked; SH-23 bypass open")
            
            self.state.step_index = 3
            
        elif step == 3:
            # Step 3: Commander directs & Planning cluster runs
            self._update_node_status("commander", "active", "Synthesizing plans & issuing orders")
            t_cmd = self.commander.synthesize_and_direct(self.state)
            self.state.reasoning_logs.append(t_cmd)
            self._update_node_status("commander", "completed", "Authorized Mass Evacuation")

            self._update_node_status("rescue_planning", "active", "Deploying NDRF and SDRF assets")
            t_rescue = self.rescue_agent.run(self.state)
            self.state.reasoning_logs.append(t_rescue)
            self._update_node_status("rescue_planning", "completed", "NDRF & SDRF deployed to coordinates")

            self._update_node_status("logistics_planning", "active", "Establishing SH-23 convoy")
            t_log = self.logistics_agent.run(self.state)
            self.state.reasoning_logs.append(t_log)
            self._update_node_status("logistics_planning", "completed", "SH-23 corridor active; shelters ready")
            
            self.state.step_index = 4
            
        elif step == 4:
            # Step 4: Communication Execution Agent generates multilingual broadcasts
            self._update_node_status("communication_execution", "active", "Generating multilingual CAP broadcast")
            t_comm = self.communication_agent.run(self.state)
            self.state.reasoning_logs.append(t_comm)
            self._update_node_status("communication_execution", "completed", "Cell Broadcast delivered (EN/HI/Pahari)")
            
            self.state.step_index = 5
            
        elif step == 5:
            # Step 5: Final command review
            self._update_node_status("commander", "active", "Auditing evacuation progress")
            t_final = self.commander.finalize_execution_review(self.state)
            self.state.reasoning_logs.append(t_final)
            self._update_node_status("commander", "completed", "Autonomous loop active")
            
            self.state.step_index = 6
            self.state.execution_completed = True
            
        return self.get_disaster_state()

    def run_full_scenario(self, rainfall: float = 145.0, slope: float = 42.0, river: float = 4.2) -> DisasterState:
        """
        Runs the complete multi-agent workflow from start to finish.
        """
        self.state = self._create_initial_state()
        self.state.telemetry.rainfall_mm_hr = rainfall
        self.state.telemetry.slope_angle_deg = slope
        self.state.telemetry.river_level_m = river
        
        while self.state.step_index < 6:
            self.execute_step()
            
        return self.get_disaster_state()

    def handle_citizen_sos(self, sos_data: Dict[str, Any]) -> DisasterState:
        """
        Dynamically handles an incoming SOS request, re-routing tactical responders.
        """
        thought = self.commander.handle_sos_escalation(self.state, sos_data)
        self.state.reasoning_logs.insert(0, thought)
        
        # Add SOS GIS feature
        sos_feature = {
            "id": f"sos_dynamic_{len(self.state.gis_features)}",
            "feature_type": "sos_beacon",
            "name": f"CITIZEN SOS: {sos_data.get('citizen_name', 'Citizen')}",
            "coordinates": [sos_data.get("lat", 31.7125), sos_data.get("lng", 76.9380)],
            "properties": {
                "requester": sos_data.get("citizen_name", "Citizen"),
                "people_count": sos_data.get("people_count", 4),
                "details": sos_data.get("emergency_details", "Trapped in flood/landslide"),
                "assigned_responder": "SDRF-QRT-2",
                "status": "DISPATCH_IN_PROGRESS",
                "pulse": True
            }
        }
        # Ingest into GIS features if not present
        from models.schemas import GISFeature
        self.state.gis_features.append(GISFeature(**sos_feature))
        
        return self.get_disaster_state()


# Global orchestrator singleton instance
orchestrator = MultiAgentOrchestrator()
