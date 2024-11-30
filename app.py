from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# API route to fetch weather data
@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')  # Get city name from query parameter
    if not city:
        return jsonify({"error": "City name is required"}), 400

    user_api = os.environ.get('test3')  # Fetch API key from environment variable
    if not user_api:
        print("API key not found")
        return jsonify({"error": "API key is not set"}), 500

    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={user_api}"
    print(f"API URL: {api_url}")  # Log API URL for debugging
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Failed API call. Status code: {response.status_code}")
        print(f"Error details: {response.text}")
        return jsonify({"error": "Failed to fetch weather data", "details": response.json()}), response.status_code

    data = response.json()
    temp_city = data['main']['temp'] - 273.15
    weather_desc = data['weather'][0]['description']
    hmdt = data['main']['humidity']
    wind_spd = data['wind']['speed']

    return jsonify({
        "temperature": f"{temp_city:.2f} °C",
        "description": weather_desc,
        "humidity": f"{hmdt}%",
        "wind_speed": f"{wind_spd} kmph"
    })

if __name__ == '__main__':
    app.run(debug=True)


