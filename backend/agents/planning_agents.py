# backend/agents/planning_agents.py
import uuid
from datetime import datetime
from models.schemas import AgentThought, AgentType, TacticalOrder, PriorityLevel
from agents.state import MultiAgentWorkflowState


class RescuePlanningAgent:
    """
    Formulates tactical SAR (Search and Rescue) mission profiles.
    Allocates NDRF, SDRF, and medical teams to specific geographic coordinates.
    """
    def __init__(self):
        self.agent_id = AgentType.RESCUE_PLANNING
        self.name = "Tactical Search & Rescue Planning Agent"
        self.role = "Tactical Asset Allocation & Multi-Force Coordination"

    def run(self, state: MultiAgentWorkflowState) -> AgentThought:
        thought_text = (
            "Synthesizing SAR operational plan for Mandi crisis: "
            "1. NDRF BATTALION 14 (BRAVO): Assigned to Sector 2 (Victoria Bridge & Beas Floodplain) with 4 inflatable "
            "Zodiac boats and hydraulic shoring gear. "
            "2. SDRF HP MOUNTAIN SQUAD (ALPHA): Assigned to Sector 1 (Bhiuli Ridge 42° Slope) with high-angle rope "
            "rigging, drone thermal reconnaissance, and stretcher evacuation teams. "
            "3. MEDICAL TRIAGE: 8 Advance Life Support (ALS) Ambulances stationed at Mandi Vallabh College staging zone. "
            "4. IAF HELICOPTER STANDBY: Requested 2 Mi-17 helicopters on 20-min standby at Mandi Ridge Helipad for roof-top extractions."
        )
        
        action = "DISPATCHED_TACTICAL_SAR_ORDERS: 48 specialized responders deployed across Bhiuli and Victoria Bridge sectors."
        
        # Create Tactical Orders
        order_ndrf = TacticalOrder(
            id=f"ORD-NDRF-{uuid.uuid4().hex[:6].upper()}",
            title="Deploy NDRF Bravo Unit to Beas Flood Basin",
            target_agency="NDRF 14th Battalion",
            priority=PriorityLevel.CRITICAL,
            action_type="DISPATCH_RESCUE",
            status="DISPATCHED",
            details="Deploy 28 rescue divers and 4 inflatable boats to extract trapped citizens in Victoria Bridge low terraces.",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            assigned_units=["NDRF-Bravo-1", "NDRF-Bravo-2", "Zodiac-Fleet-4"]
        )
        
        order_sdrf = TacticalOrder(
            id=f"ORD-SDRF-{uuid.uuid4().hex[:6].upper()}",
            title="Deploy SDRF High-Angle Mountain Squad to Bhiuli",
            target_agency="SDRF Himachal Pradesh",
            priority=PriorityLevel.CRITICAL,
            action_type="DISPATCH_RESCUE",
            status="DISPATCHED",
            details="Establish mountain anchor systems on Bhiuli 42° slope; assist 380 elderly and disabled citizens down safe trails.",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            assigned_units=["SDRF-Alpha-Lead", "Mountain-Rigging-Team-3", "Thermal-Drone-Recon"]
        )
        
        state.orders.append(order_ndrf)
        state.orders.append(order_sdrf)
        
        structured_out = {
            "ndrf_deployment": {
                "unit": "NDRF 14th Battalion Bravo",
                "personnel": 28,
                "sector": "Sector 2 - Victoria Bridge Flood Basin",
                "coordinates": [31.7070, 76.9285],
                "equipment": ["4 Inflatable Boats", "Hydraulic Cutters", "Sonar Lifeline"]
            },
            "sdrf_deployment": {
                "unit": "SDRF HP Mountain Squad Alpha",
                "personnel": 20,
                "sector": "Sector 1 - Bhiuli Landslide Ridge",
                "coordinates": [31.7175, 76.9370],
                "equipment": ["High-Angle Rope Systems", "Drone Recon", "Trauma Stretchers"]
            },
            "air_support": "2 IAF Mi-17 Choppers on standby at Ridge Helipad",
            "active_orders_issued": [order_ndrf.id, order_sdrf.id]
        }
        
        state.rescue_plan = structured_out
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=3,
            thought=thought_text,
            action_taken=action,
            confidence=0.96,
            raw_prompt_preview="PROMPT: Generate SAR force layout for 4,500 people under dual landslide/flood threat.",
            structured_output=structured_out
        )


class LogisticsPlanningAgent:
    """
    Coordinates safe evacuation corridors, transit fleets, and shelter supply logistics.
    Directs civilian movement away from blocked NH-154 onto safe SH-23 bypass.
    """
    def __init__(self):
        self.agent_id = AgentType.LOGISTICS_PLANNING
        self.name = "Evacuation Logistics & Supply Chain Agent"
        self.role = "Route Optimization, Fleet Dispatch & Shelter Management"

    def run(self, state: MultiAgentWorkflowState) -> AgentThought:
        thought_text = (
            "Computing dynamic evacuation logistics for 4,500 civilians: "
            "1. TRAFFIC DIVERSION: Mandi Traffic Police instructed to establish total roadblock at NH-154 KM 10 and KM 15. "
            "All outbound civilian and emergency convoy traffic redirected onto SH-23 High Ridge Bypass via Kataula. "
            "2. FLEET DISPATCH: 30 HRTC state buses requisitioned and dispatched to 3 assembly points at 5-minute headways. "
            "3. SHELTER PROVISIONING: Safe Refuge Center A (Vallabh College - Cap: 3000) activated with 5,000 hot meals, "
            "10,000 water pouches, and 1,200 dry blankets. Safe Center B (Ridge Camp - Cap: 2000) prepared with power generators."
        )
        
        action = "ESTABLISHED_EVACUATION_CORRIDOR_SH23: Diverted traffic from blocked NH-154; activated 30 buses and 2 safe shelters."
        
        order_police = TacticalOrder(
            id=f"ORD-TRAFFIC-{uuid.uuid4().hex[:6].upper()}",
            title="Total Roadblock NH-154 & Activate SH-23 Green Corridor",
            target_agency="HP Traffic Police & PWD",
            priority=PriorityLevel.CRITICAL,
            action_type="ROAD_CLOSURE",
            status="EXECUTED",
            details="Seal NH-154 at Mandi Victoria junction; pilot emergency evacuation convoys exclusively via SH-23 bypass.",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            assigned_units=["Traffic-Sector-North", "PWD-JCB-Team-2"]
        )
        
        order_shelter = TacticalOrder(
            id=f"ORD-SHELTER-{uuid.uuid4().hex[:6].upper()}",
            title="Activate Mandi College & Ridge Shelters",
            target_agency="District Administration & Red Cross",
            priority=PriorityLevel.HIGH,
            action_type="RATION_SUPPLY",
            status="IN_PROGRESS",
            details="Open Mandi Vallabh College Hall (Capacity 3000) and Ridge Emergency Camp (Capacity 2000). Dispense food/water.",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            assigned_units=["District-Relief-Cell", "Red-Cross-Logistics-3"]
        )
        
        state.orders.append(order_police)
        state.orders.append(order_shelter)
        
        structured_out = {
            "evacuation_corridor": "SH-23 High Ridge Bypass (Kataula Road)",
            "road_closure_directive": "NH-154 KM 12.4 Sealed",
            "evacuation_transit": {
                "hrtc_buses_deployed": 30,
                "trip_cycle_time_mins": 25,
                "estimated_evacuation_time_mins": 75
            },
            "shelter_allocation": [
                {"name": "Mandi Vallabh College Hall", "capacity": 3000, "status": "RECEIVING_CIVILIANS"},
                {"name": "Mandi Ridge Helipad Camp", "capacity": 2000, "status": "STAGED_READY"}
            ],
            "supplies_mobilized": {
                "food_rations": 5000,
                "drinking_water_pouches": 10000,
                "thermal_blankets": 1200,
                "diesel_generators": 6
            }
        }
        
        state.logistics_plan = structured_out
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=3,
            thought=thought_text,
            action_taken=action,
            confidence=0.97,
            raw_prompt_preview="PROMPT: Plan evacuation transport for 4,500 people. Factor in NH-154 closure and SH-23 capacity.",
            structured_output=structured_out
        )
