from flask import Flask, request, jsonify
from datetime import datetime
import json
import math

app = Flask(__name__)

# Simulation configurations
SENSORS_CONFIG = {
    "SEN-013": {"type": "FLOAT", "unit": "psi"},
    "SEN-015": {"type": "FLOAT", "unit": "psi"},
    "SEN-016": {"type": "FLOAT", "unit": "psi"},
    "SEN-004": {"type": "FLOAT", "unit": "mm_s"},
    "SEN-008": {"type": "FLOAT", "unit": "mm_s"},
    "SEN-023": {"type": "FLOAT", "unit": "mm_s"},
    "SEN-017": {"type": "FLOAT", "unit": "V"},
    "SEN-019": {"type": "FLOAT", "unit": "amp"},
    "SEN-030": {"type": "FLOAT", "unit": "%"},
    "SEN-026": {"type": "FLOAT", "unit": "%LEL"},
    "SEN-027": {"type": "BOOLEAN", "unit": "boolean"},
}

@app.route('/api/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        readings = data.get('readings', {})
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "simulations": []
        }
        
        # SIM-002: Well Control Pressure = max(SEN-013, SEN-015, SEN-016)
        if all(k in readings for k in ['SEN-013', 'SEN-015', 'SEN-016']):
            well_pressure = max(
                float(readings['SEN-013']),
                float(readings['SEN-015']),
                float(readings['SEN-016'])
            )
            results["simulations"].append({
                "id": "SIM-002",
                "name": "Well Control Pressure",
                "value": round(well_pressure, 2),
                "unit": "psi"
            })
        
        # SIM-006: Max Vibration = max(SEN-004, SEN-008, SEN-023)
        if all(k in readings for k in ['SEN-004', 'SEN-008', 'SEN-023']):
            max_vibration = max(
                float(readings['SEN-004']),
                float(readings['SEN-008']),
                float(readings['SEN-023'])
            )
            results["simulations"].append({
                "id": "SIM-006",
                "name": "Max Vibration",
                "value": round(max_vibration, 2),
                "unit": "mm_s"
            })
        
        # SIM-007: Real Power = 1.732 * SEN-017 * SEN-019 * 0.85 / 1000
        if all(k in readings for k in ['SEN-017', 'SEN-019']):
            real_power = 1.732 * float(readings['SEN-017']) * float(readings['SEN-019']) * 0.85 / 1000
            results["simulations"].append({
                "id": "SIM-007",
                "name": "Real Power",
                "value": round(real_power, 2),
                "unit": "kW"
            })
        
        # SIM-010: Tank Level = SEN-030
        if 'SEN-030' in readings:
            tank_level = float(readings['SEN-030'])
            results["simulations"].append({
                "id": "SIM-010",
                "name": "Tank Level",
                "value": round(tank_level, 2),
                "unit": "%"
            })
        
        # SIM-013: Emergency Logic = (SEN-026 > 25) || (SEN-027 == 1)
        if all(k in readings for k in ['SEN-026', 'SEN-027']):
            gas_level = float(readings['SEN-026'])
            esd_signal = int(readings['SEN-027'])
            emergency = (gas_level > 25) or (esd_signal == 1)
            results["simulations"].append({
                "id": "SIM-013",
                "name": "Emergency Logic",
                "value": emergency,
                "unit": "boolean"
            })
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "UP",
        "service": "Oil Gas Simulator",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)