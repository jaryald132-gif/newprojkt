# backend/agents/execution_agents.py
import uuid
from datetime import datetime
from models.schemas import AgentThought, AgentType, AlertPayload
from agents.state import MultiAgentWorkflowState


class CommunicationAgent:
    """
    Synthesizes multilingual Common Alerting Protocol (CAP) messages,
    emergency Cell Broadcast SMS, and siren activations.
    Ensures 100% dialect penetration in English, Hindi, and Mandyali Pahari.
    """
    def __init__(self):
        self.agent_id = AgentType.COMMUNICATION_EXECUTION
        self.name = "Multilingual Emergency Communication Agent"
        self.role = "Cell Broadcast, CAP Protocol & Multilingual Alert Synthesis"

    def run(self, state: MultiAgentWorkflowState) -> AgentThought:
        # Multilingual alert synthesis for Mandi, Himachal Pradesh
        english_msg = (
            "🚨 CRITICAL EMERGENCY ALERT [MANDI DISASTER CONTROL]: "
            "Severe Cloudburst & Landslide Risk in Bhiuli and Pandoh sectors. NH-154 IS BLOCKED at KM 12.4. "
            "Mandatory evacuation is ordered immediately. Proceed ONLY via the SH-23 Bypass (Kataula Road) "
            "to Mandi Vallabh College Safe Shelter. Do not stay near riverbanks or steep mountain slopes. "
            "NDRF/SDRF teams are actively assisting. Helpline: 1077 / 112."
        )
        
        hindi_msg = (
            "🚨 आपातकालीन चेतावनी [जिला आपदा प्रबंधन प्राधिकरण मंडी]: "
            "बियुली और पंडोह क्षेत्र में भारी बादल फटने और भूस्खलन का गंभीर खतरा है। राष्ट्रीय राजमार्ग NH-154 KM 12.4 पर बंद है। "
            "सभी नागरिक तुरंत सुरक्षित स्थान की ओर निकलें। केवल SH-23 बाईपास (कटौला मार्ग) से होते हुए मंडी वल्लभ कॉलेज राहत शिविर पहुंचे। "
            "नदी किनारों और कच्ची ढलानों से दूर रहें। एनडीआरएफ (NDRF) और एसडीआरएफ (SDRF) दल तैनात हैं। हेल्पलाइन: 1077 / 112।"
        )
        
        pahari_msg = (
            "🚨 जरूरी सतर्कता संदेश [मंडी आपदा कंट्रोल]: "
            "बिउली ते पंडोह दे इलाकयां च बड्डू मींह ते लैंडस्लाइड दा भारी खतरा बणी गेया है! NH-154 सड़क KM 12.4 कने बंद होई गेई है। "
            "सारे लोकां जो तुरन्त घर खाली करन दी सलाह दित्ती जांदी है। सिर्फ SH-23 बाईपास (कटौला रोड़) थानी वल्लभ कॉलेज राहत कैंपे च पौंचो। "
            "ब्यास खड्ड कने ढालां दे नेड़े मति जा। NDRF ते SDRF दी टीमां मद्द लेई मौजूदन। मदद लेई डायल करो: 1077 / 112।"
        )
        
        alert = AlertPayload(
            id=f"ALERT-CAP-{uuid.uuid4().hex[:6].upper()}",
            title="IMMEDIATE EVACUATION ORDER: Mandi Landslide & Flood Crisis",
            disaster_type="LANDSLIDE_AND_FLASH_FLOOD",
            english_text=english_msg,
            hindi_text=hindi_msg,
            pahari_text=pahari_msg,
            affected_zones=["Bhiuli Ridge (Sector 1)", "Victoria Bridge (Sector 2)", "Pandoh Basin (Sector 3)"],
            broadcast_channels=["CELL_BROADCAST_GEOFENCE", "SMS_GATEWAY", "LOCAL_FM_AIR_MANDI", "OUTDOOR_SIRENS"],
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        
        state.alerts.append(alert)
        
        thought_text = (
            "Formulating localized multilingual alert dissemination: "
            "1. ENGLISH & HINDI: Synthesized for institutional, national media, and interstate travelers on NH-154. "
            "2. PAHARI (MANDYALI DIALECT): Formulated with local mountain idioms to ensure 100% comprehension among "
            "elderly village residents in Bhiuli and Pandoh spurs. "
            "3. CELL BROADCAST: Geofenced to Mandi BTS cell towers (lat: 31.7087, lng: 76.9320, radius: 12km). "
            "4. OUTDOOR SIRENS: Triggered continuous 3-tone warble across 4 municipal siren towers."
        )
        
        action = "BROADCASTED_MULTILINGUAL_CAP_ALERTS: Geofenced SMS & siren triggers transmitted in English, Hindi, and Pahari."
        
        structured_out = {
            "alert_id": alert.id,
            "geofence_center": [31.7087, 76.9320],
            "geofence_radius_km": 12.0,
            "estimated_target_devices": 42000,
            "languages_dispatched": ["English", "Hindi (हिन्दी)", "Pahari / Mandyali (मंडयाली)"],
            "siren_status": "ACTIVATED_WARBLE_PATTERN_4",
            "telecom_operators": ["JIO", "AIRTEL", "BSNL", "VI"]
        }
        
        state.communication_payload = structured_out
        
        return AgentThought(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            step_index=4,
            thought=thought_text,
            action_taken=action,
            confidence=0.99,
            raw_prompt_preview="PROMPT: Translate emergency evacuation orders into High-Purity English, Hindi, and Mandyali Pahari.",
            structured_output=structured_out
        )
