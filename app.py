from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_BASE = "http://46.250.239.109:6001/api/uids"
SESSION_COOKIE = ".eJyrVoovSC3KTcxLzStRsiopKk3VUSrKz0lVslIqLU4tUtIBU_GZKUpWRgZGEF5eYi5IPs-gLDE-I7VCqRYAP14XTw.aa0L4A.X9I-0xcVM1yjXODjdiHutIxSJeQ"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return "OK", 200

@app.route('/api/sync-uid', methods=['POST'])
def sync_uid():
    data = request.json
    uid = data.get('uid')
    hours = data.get('hours')
    
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"session={SESSION_COOKIE}",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        payload = {
            "uid": uid, 
            "duration_hours": int(hours), 
            "cost": 0.0
        }
        resp = requests.post(API_BASE, json=payload, headers=headers, timeout=10)

        if resp.status_code in [200, 201, 204]:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": f"Server Error: {resp.status_code}"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Render dynamic port binding fix
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
