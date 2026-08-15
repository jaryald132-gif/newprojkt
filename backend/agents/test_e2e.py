# backend/test_e2e.py
import urllib.request
import json
import asyncio
import websockets

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/stream"


def test_http():
    print("--- 1. Testing REST Endpoints ---")
    
    # Root
    with urllib.request.urlopen(f"{BASE_URL}/") as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] GET / -> {data['project']} ({data['status']})")

    # Health
    with urllib.request.urlopen(f"{BASE_URL}/api/health") as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] GET /api/health -> {data['status']} (Agents Ready: {data['agents_ready']})")

    # Initial State
    with urllib.request.urlopen(f"{BASE_URL}/api/scenario/state") as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] GET /api/scenario/state -> {data['scenario_name']} (Step: {data['current_step']})")

    # Reset
    req = urllib.request.Request(f"{BASE_URL}/api/scenario/reset", data=b"", method="POST")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] POST /api/scenario/reset -> Current Step: {data['current_step']}")

    # Step-by-Step execution
    req = urllib.request.Request(f"{BASE_URL}/api/scenario/step", data=b"", method="POST")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] POST /api/scenario/step -> Current Step: {data['current_step']}, Reasonings: {len(data['reasoning_logs'])}")

    # Trigger Full Scenario
    payload = json.dumps({"rainfall_mm_hr": 150.0, "slope_deg": 43.0, "river_level_m": 4.5}).encode()
    req = urllib.request.Request(f"{BASE_URL}/api/scenario/trigger", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] POST /api/scenario/trigger -> Completed: {data['execution_completed']}, Orders: {len(data['orders'])}, Alerts: {len(data['alerts'])}")

    # SOS Distress Simulation
    sos_payload = json.dumps({
        "citizen_name": "Devendra Sharma",
        "lat": 31.7140,
        "lng": 76.9390,
        "contact": "+91 98160-54321",
        "people_count": 5,
        "emergency_details": "Water level rising near shop, road blocked.",
        "medical_needed": False
    }).encode()
    req = urllib.request.Request(f"{BASE_URL}/api/simulate/sos", data=sos_payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] POST /api/simulate/sos -> Latest Order: {data['orders'][0]['title']}")

    # Agent Topology Graph
    with urllib.request.urlopen(f"{BASE_URL}/api/agents/graph") as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        print(f" [PASS] GET /api/agents/graph -> Nodes: {len(data['nodes'])}, Links: {len(data['links'])}")


async def test_websocket():
    print("\n--- 2. Testing Live WebSocket Stream ---")
    async with websockets.connect(WS_URL) as ws:
        msg = await ws.recv()
        data = json.loads(msg)
        print(f" [PASS] WebSocket Connected -> Initial Event: {data['event']}")

        await ws.send(json.dumps({"action": "RESET"}))
        msg = await ws.recv()
        data = json.loads(msg)
        print(f" [PASS] WS Action 'RESET' -> Broadcast Event: {data['event']}")

        await ws.send(json.dumps({"action": "STEP"}))
        msg = await ws.recv()
        data = json.loads(msg)
        print(f" [PASS] WS Action 'STEP' -> Broadcast Event: {data['event']}, Step: {data['state']['current_step']}")


if __name__ == "__main__":
    test_http()
    asyncio.run(test_websocket())
    print("\n*** ALL BACKEND ENDPOINTS AND WEBSOCKETS VERIFIED END-TO-END ***")
