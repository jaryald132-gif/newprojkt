# backend/agents/commander_agent.py
import uuid
from datetime import datetime
from typing import Dict, Any, List
from models.schemas import (
    AgentThought,
    AgentType,
    TacticalOrder,
    PriorityLevel,
    DisasterStatus
)
from agents.state import MultiAgentWorkflowState


class CommanderAgent:
    """
    The Orchestrating Mind (AI Commander).
    Synthesizes incoming data streams from sub-agents, resolves operational tradeoffs,
    issues executive directives, and oversees end-to-end response execution.
    """
    def __init__(self):
        self.agent_id = AgentType.COMMANDER
        self.name = "ASCENDANT AI Commander"
        self.role = "Strategic Incident Commander & Multi-Agent Orchestrator"

    def initial_assessment(self, state: MultiAgentWorkflowState) -> AgentThought:
        thought_text = (
            "INCIDENT ACTIVATION: Early warning sensors in Mandi, Himachal Pradesh detect extreme anomaly. "
            "Telemetry shows 145mm/hr precipitation on saturated 42° mountain slopes above NH-154. "
            "Directing Risk Detection Agents (Weather, Terrain, Hydrology) to immediately assess failure horizons. "
            "Setting disaster threat level to RED_ALERT_LEVEL_4."
        )
        
        action = "DISASTER_COORDINATION_INITIATED: Activated multi-agent reconnaissance protocol for Mandi Valley."
        
        state.status = DisasterStatus.CRITICAL
        state.threat_level = "RED_ALERT_LEVEL_4"
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=0,
            thought=thought_text,
            action_taken=action,
            confidence=0.99,
            raw_prompt_preview="PROMPT: Commander, evaluate sensor triggers for Mandi, HP. Initiate multi-agent tasking.",
            structured_output={
                "directive": "INITIATE_MULTI_AGENT_RESPONSE",
                "target_location": "Mandi, Himachal Pradesh",
                "assigned_agents": ["WeatherRiskAgent", "TerrainRiskAgent", "FloodRiskAgent"]
            }
        )

    def synthesize_and_direct(self, state: MultiAgentWorkflowState) -> AgentThought:
        # Ingest assessments from sub-agents
        pop = state.telemetry.population_at_risk
        
        thought_text = (
            f"SYNTHESIZING MULTI-AGENT INTELLIGENCE: "
            f"Risk agents confirm critical cloudburst (145mm/hr) and catastrophic slope instability on 42° slope. "
            f"Impact agents report NH-154 blocked at KM 12.4 with {pop:,} civilians trapped across 3 vulnerable sectors. "
            f"EXECUTIVE DECISION: Authorizing mandatory evacuation of {pop:,} residents via SH-23 High Ridge Bypass. "
            f"Directing RescuePlanningAgent to mobilize NDRF 14th Bn & SDRF Alpha squads immediately. "
            f"Directing CommunicationAgent to broadcast multilingual alerts in English, Hindi, and Mandyali Pahari."
        )
        
        action = f"EXECUTIVE_COMMAND_ISSUED: Mandatory evacuation of 4,500 people authorized; SAR and alert execution approved."
        
        # Add Commander Supreme Directive Order
        supreme_order = TacticalOrder(
            id=f"ORD-EXEC-{uuid.uuid4().hex[:6].upper()}",
            title="EXECUTIVE MANDATE: Total Mandi Valley Emergency Evacuation",
            target_agency="Joint Unified Command (DC Mandi / NDRF / SDRF / Police)",
            priority=PriorityLevel.CRITICAL,
            action_type="EVACUATION",
            status="IN_PROGRESS",
            details=f"Execute synchronized evacuation of {pop:,} civilians across Sectors 1, 2, 3 via SH-23 bypass to safe shelters.",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            assigned_units=["Joint-Ops-HQ", "NDRF-14-Bn", "SDRF-HP", "HP-Police", "HRTC-Fleet"]
        )
        
        state.orders.insert(0, supreme_order)
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=3,
            thought=thought_text,
            action_taken=action,
            confidence=0.99,
            raw_prompt_preview="PROMPT: Commander, synthesize Risk and Impact findings. Issue executive disaster directives.",
            structured_output={
                "operational_phase": "EXECUTION_AND_MASS_EVACUATION",
                "evacuation_scope": f"{pop} citizens",
                "lifeline_corridor": "SH-23 High Ridge Bypass",
                "command_status": "BINDING_DIRECTIVE_ENFORCED"
            }
        )

    def finalize_execution_review(self, state: MultiAgentWorkflowState) -> AgentThought:
        evac_count = state.telemetry.evacuated_count + 1850
        state.telemetry.evacuated_count = min(evac_count, state.telemetry.population_at_risk)
        
        thought_text = (
            "POST-ACTION COMMAND REVIEW: "
            "All tactical plans successfully translated into field operations. "
            "1. Cell Broadcast SMS delivered to ~42,000 devices in English, Hindi, and Mandyali. "
            "2. Traffic diversion at NH-154 active; 30 HRTC evacuation buses running convoy on SH-23. "
            "3. NDRF and SDRF teams currently on-scene conducting boat rescues and mountain rigging. "
            "Evacuation is progressing safely with zero reported fatalities. ASCENDANT Multi-Agent loop nominal."
        )
        
        action = "RESPONSE_LIFECYCLE_ACTIVE: Multi-agent execution loop stabilized; continuous monitoring mode enabled."
        
        state.execution_completed = True
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=5,
            thought=thought_text,
            action_taken=action,
            confidence=1.0,
            raw_prompt_preview="PROMPT: Commander, audit deployment logs, casualty mitigation, and operational continuity.",
            structured_output={
                "system_status": "AUTONOMOUS_EXECUTION_SUCCESS",
                "evacuation_progress": f"{state.telemetry.evacuated_count} / {state.telemetry.population_at_risk} safely moved",
                "active_operations": 5,
                "multi_agent_sync": "100%_COORDINATED"
            }
        )

    def handle_sos_escalation(self, state: MultiAgentWorkflowState, sos_data: Dict[str, Any]) -> AgentThought:
        citizen = sos_data.get("citizen_name", "Citizen")
        people = sos_data.get("people_count", 4)
        lat = sos_data.get("lat", 31.7125)
        lng = sos_data.get("lng", 76.9380)
        
        thought_text = (
            f"DYNAMIC SOS INTERCEPTION: Priority emergency distress beacon received from {citizen} "
            f"({people} individuals trapped at lat: {lat:.4f}, lng: {lng:.4f} near Victoria Bridge). "
            f"AI Commander executing real-time tactical reroute: Reassigning SDRF Squad Alpha Quick-Response Unit "
            f"from secondary perimeter to immediate extraction at target coordinates."
        )
        
        action = f"DYNAMIC_REPLAN_EXECUTED: Dispatched SDRF QRT to extract {people} trapped civilians at SOS coordinates."
        
        sos_order = TacticalOrder(
            id=f"ORD-SOS-{uuid.uuid4().hex[:6].upper()}",
            title=f"URGENT EXTRACTION: {citizen} ({people} persons)",
            target_agency="SDRF Quick Response Squad",
            priority=PriorityLevel.CRITICAL,
            action_type="DISPATCH_RESCUE",
            status="DISPATCHED",
            details=f"Immediate rescue at coordinates [{lat}, {lng}]. Medical assistance required.",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            assigned_units=["SDRF-QRT-2", "ALS-Ambulance-4"]
        )
        
        state.orders.insert(0, sos_order)
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=6,
            thought=thought_text,
            action_taken=action,
            confidence=0.99,
            raw_prompt_preview=f"PROMPT: Incoming SOS from {citizen} ({people} people). Re-route closest tactical unit.",
            structured_output={
                "sos_processed": True,
                "requester": citizen,
                "rescuer_assigned": "SDRF-QRT-2",
                "eta_minutes": 7
            }
        )
