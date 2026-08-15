# backend/agents/risk_agents.py
import uuid
from datetime import datetime
from models.schemas import AgentThought, AgentType
from agents.state import MultiAgentWorkflowState


class WeatherRiskAgent:
    """
    Ingests simulated Doppler radar and meteorological sensors for Mandi, HP.
    Detects extreme rainfall / cloudburst conditions.
    """
    def __init__(self):
        self.agent_id = AgentType.WEATHER_RISK
        self.name = "Meteorological Risk Detection Agent"
        self.role = "Atmospheric Sensing & Cloudburst Radar Analysis"

    def run(self, state: MultiAgentWorkflowState) -> AgentThought:
        rain = state.telemetry.rainfall_mm_hr
        
        # LLM-simulated structured reasoning
        thought_text = (
            f"Ingesting Mandi Doppler Radar RR-02: Instantaneous precipitation measured at {rain:.1f} mm/hr. "
            "Exceeds IMD Extreme Cloudburst Threshold (>100mm/hr). Radar reflectivity exceeds 58 dBZ over "
            "the Bhiuli-Pandoh corridor. Convective storm cell is quasi-stationary with high water vapor flux."
        )
        
        action = f"FLAGGED_CRITICAL_CLOUDBURST: Precipitation rate {rain:.1f} mm/hr with 98% probability of flash debris ignition."
        
        structured_out = {
            "radar_station": "MANDI_RIDGE_RR-02",
            "rainfall_rate_mm_hr": rain,
            "cloudburst_detected": True,
            "storm_cell_velocity_kmh": 4.5,
            "estimated_duration_hours": 3.5,
            "atmospheric_risk_index": "SEVERE_LEVEL_5",
            "target_geography": "Bhiuli - Pandoh - Victoria Bridge Basin"
        }
        
        state.weather_risk_assessment = structured_out
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=1,
            thought=thought_text,
            action_taken=action,
            confidence=0.98,
            raw_prompt_preview="PROMPT: Analyze Mandi Doppler Radar Doppler DBZ: 58.2 | Rain: 145mm/hr. Classify event and trigger envelope.",
            structured_output=structured_out
        )


class TerrainRiskAgent:
    """
    Evaluates geotechnical slope stability on Mandi mountain Ghats (42° slope).
    """
    def __init__(self):
        self.agent_id = AgentType.TERRAIN_RISK
        self.name = "Geotechnical Slope Stability Agent"
        self.role = "GIS Digital Elevation Model & Inclinometer Ingestion"

    def run(self, state: MultiAgentWorkflowState) -> AgentThought:
        slope = state.telemetry.slope_angle_deg
        moisture = state.telemetry.soil_moisture_pct
        
        # Geotechnical Factor of Safety (FoS) estimation
        fos = round(0.68 * (45.0 / slope) * (100.0 - moisture) / 20.0, 2)
        if fos > 1.2:
            fos = 0.65  # Saturated condition override
        
        thought_text = (
            f"Processing DEM 10m contour grid for Mandi Bhiuli slope (Inclination: {slope:.1f}°). "
            f"Borehole Inclinometer SI-09 reports subsurface shear displacement of 41mm/hr. "
            f"Soil pore-water saturation is {moisture:.1f}%. "
            f"Computed Factor of Safety (FoS) = {fos} (< 1.0 implies imminent catastrophic slope failure). "
            "High vulnerability for high-velocity debris avalanche directly intersecting National Highway 154."
        )
        
        action = f"TRIGGERED_LANDSLIDE_RED_ALERT: Mass wasting hazard critical on 42° slope over NH-154 KM 12.4."
        
        structured_out = {
            "slope_angle_deg": slope,
            "soil_saturation_pct": moisture,
            "factor_of_safety": fos,
            "slope_stability_status": "IMMINENT_SLOPE_COLLAPSE",
            "debris_volume_potential_m3": 18500,
            "shear_velocity_mm_hr": 41.2,
            "critical_choke_point": "NH-154 KM 12.4 (Bhiuli Spur)"
        }
        
        state.terrain_slope_assessment = structured_out
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=1,
            thought=thought_text,
            action_taken=action,
            confidence=0.96,
            raw_prompt_preview=f"PROMPT: Ingest Inclinometer SI-09: Slope={slope}°, Saturation={moisture}%. Calculate Mohr-Coulomb shear failure.",
            structured_output=structured_out
        )


class FloodRiskAgent:
    """
    Monitors Beas River hydrology and Pandoh Dam discharge.
    """
    def __init__(self):
        self.agent_id = AgentType.FLOOD_RISK
        self.name = "Hydrological Flood Detection Agent"
        self.role = "River Hydrodynamics & Inundation Modeling"

    def run(self, state: MultiAgentWorkflowState) -> AgentThought:
        river_level = state.telemetry.river_level_m
        danger_mark = state.telemetry.river_danger_level_m
        delta = round(river_level - danger_mark, 2)
        
        thought_text = (
            f"Beas River Hydro Gauge RG-04 at Victoria Bridge reports water level of {river_level:.2f}m "
            f"(+{delta:.2f}m ABOVE DANGER MARK). Upstream discharge rate from Pandoh catchment stands at 84,000 cusecs. "
            "Hydrodynamic model indicates backwater surging at confluence channels, inundating ground-level structures "
            "and undermining road retaining embankments."
        )
        
        action = f"ISSUED_FLASH_FLOOD_SURCHARGE_ALARM: River Beas running {delta:.2f}m above danger mark."
        
        structured_out = {
            "river_level_meters": river_level,
            "danger_threshold_meters": danger_mark,
            "surcharge_delta_meters": delta,
            "current_discharge_cusecs": 84000,
            "flood_severity": "HIGH_SURGE",
            "inundated_landmarks": ["Victoria Bridge Low Terrace", "Panchvaktra Riverside Enclave", "Pandoh Old Market"]
        }
        
        state.flood_hydrology_assessment = structured_out
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=1,
            thought=thought_text,
            action_taken=action,
            confidence=0.94,
            raw_prompt_preview="PROMPT: Analyze RG-04 Hydrograph: 4.2m level vs 3.0m danger. Predict 60-min flood wave propagation.",
            structured_output=structured_out
        )
