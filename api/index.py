from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Credenciales Smartcar
CLIENT_ID = "56f8dcaa-9ef4-4f25-a992-ca00c68b8bfb"
SMARTCAR_API = "https://api.smartcar.com/v2.0"

# Aquí irá el Access Token (obtenido del flujo OAuth)
ACCESS_TOKEN = None

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """Obtiene vehículos de Smartcar"""
    
    if not ACCESS_TOKEN:
        return jsonify({"error": "No access token provided"}), 401
    
    try:
        # Obtener lista de vehículos
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{SMARTCAR_API}/vehicles",
            headers=headers
        )
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch vehicles"}), response.status_code
        
        vehicles_data = response.json()
        vehicles_ids = vehicles_data.get("vehicles", [])
        
        coches = []
        
        for vehicle_id in vehicles_ids[:20]:  # Limitar a 20 vehículos
            try:
                # Obtener atributos del vehículo
                vehicle_response = requests.get(
                    f"{SMARTCAR_API}/vehicles/{vehicle_id}/attributes",
                    headers=headers
                )
                
                if vehicle_response.status_code == 200:
                    attr = vehicle_response.json()
                    
                    # Obtener odómetro/km
                    odometer_response = requests.get(
                        f"{SMARTCAR_API}/vehicles/{vehicle_id}/odometer",
                        headers=headers
                    )
                    
                    km = 0
                    if odometer_response.status_code == 200:
                        km = odometer_response.json().get("distance", {}).get("value", 0)
                    
                    coche = {
                        "marca": attr.get("make", "Unknown"),
                        "modelo": attr.get("model", "Unknown"),
                        "año": attr.get("year", 0),
                        "km": int(km),
                        "precio": 0,  # Smartcar no proporciona precio
                        "combustible": attr.get("fuelType", "Unknown"),
                        "id": vehicle_id
                    }
                    coches.append(coche)
            except Exception as e:
                print(f"Error fetching vehicle {vehicle_id}: {e}")
                continue
        
        return jsonify(coches)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/set-token', methods=['POST'])
def set_token():
    """Establece el Access Token"""
    global ACCESS_TOKEN
    data = request.json
    ACCESS_TOKEN = data.get("token")
    return jsonify({"status": "Token set"}), 200


@app.route('/api/vehicles/local', methods=['GET'])
def get_local_vehicles():
    """Devuelve vehículos desde coches.json (fallback)"""
    try:
        with open('coches.json', 'r') as f:
            coches = json.load(f)
        return jsonify(coches)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚗 Servidor iniciado en http://localhost:5000")
    print("📌 Para usar Smartcar, envía un POST a /api/set-token con tu Access Token")
    app.run(debug=True, port=5000, host='localhost')

# Vercel handler
import serverless_wsgi

def handler(event, context):
    return serverless_wsgi.handle(event, context, app)
