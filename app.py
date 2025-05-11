from flask import Flask, request, jsonify
import pickle
import requests

app = Flask(__name__)

# Load model, vectorizer, and label encoder
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

# Safe Browsing API key
API_KEY = 'AIzaSyArjzKs9vN66fY_vZ-x0XSoxMLjTRhnsJM'

def check_with_safe_browsing(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    payload = {
        "client": {
            "clientId": "cyber_shield_app",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code != 200:
            print("Safe Browsing API error:", response.status_code, response.text)
            return None

        result = response.json()
        return bool(result)
    except Exception as e:
        print("Exception during Safe Browsing check:", e)
        return None

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Cyber Shield API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({"error": "URL missing in request"}), 400

    url = data['url']

    # Safe Browsing check
    is_malicious = check_with_safe_browsing(url)
    if is_malicious is True:
        return jsonify({
            "url": url,
            "prediction": "malicious",
            "confidence": "High",
            "source": "Google Safe Browsing"
        })
    elif is_malicious is None:
        print("Safe Browsing failed, falling back to ML model...")

    # ML model prediction
    vectorized_url = vectorizer.transform([url])
    prediction_encoded = model.predict(vectorized_url)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

    return jsonify({
        "url": url,
        "prediction": prediction_label,
        "confidence": "Moderate",
        "source": "ML Model"
    })

# Do not include app.run() when deploying to Render!
