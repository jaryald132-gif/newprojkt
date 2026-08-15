# backend/data/mandi_gis.py
from typing import List
from models.schemas import GISFeature, TelemetryData


def get_initial_telemetry() -> TelemetryData:
    return TelemetryData(
        rainfall_mm_hr=145.0,
        slope_angle_deg=42.0,
        river_level_m=4.2,
        river_danger_level_m=3.0,
        soil_moisture_pct=94.5,
        population_at_risk=4500,
        evacuated_count=1240,
        active_responders_count=48,
        nh154_status="BLOCKED_LANDSLIDE_KM12_4",
        sh23_status="ACTIVE_EVACUATION_CORRIDOR",
        weather_condition="Monsoon Cloudburst - Severe Inundation",
        last_updated="Just now (Live Telemetry)"
    )


def get_initial_gis_features() -> List[GISFeature]:
    return [
        # 1. SEVERE HAZARD ZONE: Bhiuli Slope & Landslide Scar (Red Polygon)
        GISFeature(
            id="zone_severe_landslide_bhiuli",
            feature_type="hazard_zone",
            name="Severe Landslide Threat Zone - Bhiuli Ridge (Slope 42°)",
            coordinates=[
                [31.7190, 76.9360],
                [31.7220, 76.9420],
                [31.7160, 76.9480],
                [31.7120, 76.9430],
                [31.7130, 76.9370],
                [31.7190, 76.9360]
            ],
            properties={
                "severity": "CRITICAL",
                "color": "#ef4444",
                "fillColor": "#dc2626",
                "fillOpacity": 0.45,
                "slope_deg": 42.0,
                "risk_factor": "Debris Flow & Mass Wasting Hazard",
                "population_exposed": 2800,
                "description": "Massive slope instability triggered by 145mm/hr torrential rain on 42° weathered sandstone/phyllite slope."
            }
        ),

        # 2. MODERATE HAZARD ZONE: Beas River Flood Basin (Amber Polygon)
        GISFeature(
            id="zone_moderate_flood_beas",
            feature_type="moderate_zone",
            name="Moderate Flash Flood Hazard Zone - Beas River Basin",
            coordinates=[
                [31.7060, 76.9250],
                [31.7110, 76.9300],
                [31.7140, 76.9340],
                [31.7100, 76.9390],
                [31.7050, 76.9330],
                [31.7020, 76.9270],
                [31.7060, 76.9250]
            ],
            properties={
                "severity": "HIGH",
                "color": "#f59e0b",
                "fillColor": "#d97706",
                "fillOpacity": 0.35,
                "river_level_m": 4.2,
                "risk_factor": "Rapid River Surcharge (1.2m above danger level)",
                "population_exposed": 1700,
                "description": "Beas River swelling rapidly from upstream Pandoh Dam discharge. Low-lying riverside enclaves inundated."
            }
        ),

        # 3. SAFE REFUGE ZONE 1: Mandi Vallabh Degree College Ground (Green Polygon)
        GISFeature(
            id="zone_safe_shelter_college",
            feature_type="safe_zone",
            name="Safe Evacuation Center A - Mandi Vallabh College High Ground",
            coordinates=[
                [31.7030, 76.9300],
                [31.7055, 76.9315],
                [31.7045, 76.9345],
                [31.7015, 76.9330],
                [31.7030, 76.9300]
            ],
            properties={
                "severity": "SAFE",
                "color": "#10b981",
                "fillColor": "#059669",
                "fillOpacity": 0.4,
                "capacity": 3000,
                "current_occupancy": 820,
                "supplies_ready": "Food rations, 500 blankets, Medical triage center active",
                "description": "Elevated terrace safe from flash floods and slope slides. Central aid distribution hub."
            }
        ),

        # 4. SAFE REFUGE ZONE 2: Mandi Ridge Helipad & Relief Camp (Green Polygon)
        GISFeature(
            id="zone_safe_shelter_ridge",
            feature_type="safe_zone",
            name="Safe Evacuation Center B - Mandi Ridge Emergency Camp",
            coordinates=[
                [31.6980, 76.9360],
                [31.7010, 76.9380],
                [31.7000, 76.9420],
                [31.6965, 76.9400],
                [31.6980, 76.9360]
            ],
            properties={
                "severity": "SAFE",
                "color": "#10b981",
                "fillColor": "#059669",
                "fillOpacity": 0.4,
                "capacity": 2000,
                "current_occupancy": 420,
                "supplies_ready": "IAF Chopper Landing Zone, Satellite Comm link active",
                "description": "High ridge designated for emergency airlift evacuation and vulnerable patient stabilization."
            }
        ),

        # 5. ROAD CLOSURE / HAZARD POINT: NH-154 KM 12.4
        GISFeature(
            id="marker_blockage_nh154",
            feature_type="road_block",
            name="CRITICAL ROAD BLOCKAGE: NH-154 KM 12.4 (Landslide)",
            coordinates=[31.7145, 76.9412],
            properties={
                "road_name": "NH-154 (Chandigarh - Manali National Highway)",
                "status": "TOTAL_CLOSURE",
                "debris_volume": "18,500 m³ rock and mudslide",
                "blocked_distance": "140 meters",
                "action": "Traffic halted. Police checkpoint established. JCB excavators dispatched."
            }
        ),

        # 6. BLOCKED HIGHWAY SEGMENT (Red Polyline)
        GISFeature(
            id="route_nh154_blocked_segment",
            feature_type="hazard_route",
            name="NH-154 Blocked Road Corridor",
            coordinates=[
                [31.7110, 76.9370],
                [31.7145, 76.9412],
                [31.7180, 76.9445],
                [31.7210, 76.9480]
            ],
            properties={
                "color": "#ef4444",
                "weight": 5,
                "dashArray": "8, 8",
                "status": "IMPASSABLE"
            }
        ),

        # 7. SAFE EVACUATION CORRIDOR: SH-23 Bypass (Emerald Polyline)
        GISFeature(
            id="route_sh23_evacuation_corridor",
            feature_type="evacuation_route",
            name="Designated Safe Evacuation Corridor (SH-23 High Ridge Bypass)",
            coordinates=[
                [31.7200, 76.9320],
                [31.7160, 76.9290],
                [31.7110, 76.9270],
                [31.7050, 76.9290],
                [31.7020, 76.9315],
                [31.6980, 76.9360]
            ],
            properties={
                "color": "#10b981",
                "weight": 6,
                "status": "OPEN_PILOTED_CONVOY",
                "travel_time_est": "18 mins to Safe Staging Zone",
                "patrolled_by": "Himachal Pradesh Traffic Police & SDRF Quick Escort"
            }
        ),

        # 8. RESPONDER UNIT: NDRF 14th Battalion Bravo Team
        GISFeature(
            id="unit_ndrf_bravo",
            feature_type="responder_unit",
            name="NDRF Battalion 14 - Unit Bravo",
            coordinates=[31.7070, 76.9285],
            properties={
                "agency": "NDRF (National Disaster Response Force)",
                "strength": 28,
                "equipment": "4 Inflatable Zodiac Boats, Hydraulic Cutters, Satellite Comm",
                "mission": "Urban Search & Rescue at Beas Floodplain & Bhiuli Access",
                "status": "EN_ROUTE_SECTOR_3",
                "callsign": "BRAVO-LEADER-1"
            }
        ),

        # 9. RESPONDER UNIT: SDRF HP Mountain Rescue Alpha Team
        GISFeature(
            id="unit_sdrf_alpha",
            feature_type="responder_unit",
            name="SDRF Himachal Pradesh - Mountain Squad Alpha",
            coordinates=[31.7175, 76.9370],
            properties={
                "agency": "SDRF (State Disaster Response Force)",
                "strength": 20,
                "equipment": "High-Angle Rope Rescue Kits, Drone Recon Team, 2 All-Terrain Ambulances",
                "mission": "Evacuation corridor pilot escort & landslide slope monitoring",
                "status": "ENGAGED_EVACUATION",
                "callsign": "ALPHA-MOUNTAIN-2"
            }
        ),

        # 10. SENSOR NODE: Doppler Rain Radar Mandi (RR-02)
        GISFeature(
            id="sensor_radar_mandi",
            feature_type="sensor_node",
            name="Doppler Rain Gauge Station RR-02 (Mandi Ridge)",
            coordinates=[31.7030, 76.9350],
            properties={
                "sensor_type": "Precipitation Doppler Radar",
                "reading": "145.2 mm/hr (Extreme Precipitation)",
                "status": "ALERT_SURGE",
                "trend": "Peak cloudburst intensity sustained"
            }
        ),

        # 11. SENSOR NODE: Geotechnical Slope Inclinometer SI-09
        GISFeature(
            id="sensor_inclinometer_bhiuli",
            feature_type="sensor_node",
            name="Slope Inclinometer SI-09 (Bhiuli Scar)",
            coordinates=[31.7160, 76.9410],
            properties={
                "sensor_type": "Borehole Slope Inclinometer & Piezometer",
                "reading": "42° Incline | Shear displacement: 41 mm/hr",
                "status": "CRITICAL_FAILURE_RISK",
                "soil_saturation": "94.5%"
            }
        ),

        # 12. SENSOR NODE: River Gauge Beas (RG-04)
        GISFeature(
            id="sensor_river_beas",
            feature_type="sensor_node",
            name="River Hydrology Gauge RG-04 (Victoria Bridge / Beas River)",
            coordinates=[31.7095, 76.9310],
            properties={
                "sensor_type": "Acoustic River Level & Discharge Gauge",
                "reading": "4.20 meters (Danger threshold: 3.00m)",
                "status": "SURCHARGE_ACTIVE",
                "discharge_rate": "84,000 cusecs"
            }
        ),

        # 13. CITIZEN SOS BEACON: Victoria Bridge Enclave
        GISFeature(
            id="sos_beacon_victoria",
            feature_type="sos_beacon",
            name="Emergency SOS Beacon #MND-882 (Victoria Bridge)",
            coordinates=[31.7125, 76.9380],
            properties={
                "requester": "Ramesh Kumar & 5 family members",
                "status": "DISPATCH_ASSIGNED",
                "assigned_to": "SDRF Squad Alpha Unit 2",
                "emergency_note": "Ground floor flooded by debris water. Need immediate evacuation.",
                "timestamp": "10:35 AM"
            }
        )
    ]
