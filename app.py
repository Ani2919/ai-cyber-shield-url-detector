from flask import Flask, request, jsonify
import pickle
import requests
from bs4 import BeautifulSoup
import tldextract

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

# 🧠 DAA-based heuristic analyzer
def run_daa_analysis(url):
    heuristic_score = 0
    reason_list = []

    # 1. Redirection check
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        redirections = len(response.history)
        if redirections > 2:
            heuristic_score += 1
            reason_list.append("Too many redirects")
    except:
        reason_list.append("URL unreachable")

    # 2. Shortened URL detection
    shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co']
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    if domain in shorteners:
        heuristic_score += 1
        reason_list.append("Shortened URL detected")

    # 3. Fake login form detection
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")
        if soup.find("input", {"type": "password"}) and any(kw in url.lower() for kw in ["login", "signin", "account", "verify"]):
            heuristic_score += 1
            reason_list.append("Fake login form detected")
    except:
        reason_list.append("HTML content parsing failed")

    # 4. Suspicious JavaScript detection
    try:
        scripts = soup.find_all("script")
        for s in scripts:
            if s.string and any(code in s.string for code in ["eval(", "document.write(", "window.location"]):
                heuristic_score += 1
                reason_list.append("Suspicious JavaScript detected")
                break
    except:
        reason_list.append("Script scan failed")

    return heuristic_score, reason_list

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Cyber Shield API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({"error": "URL missing in request"}), 400

    url = data['url']
    prediction = "benign"
    confidence = "Low"
    source = "None"
    daa_reasons = []

    # Step 1: Google Safe Browsing
    is_malicious = check_with_safe_browsing(url)
    if is_malicious is True:
        return jsonify({
            "url": url,
            "prediction": "malicious",
            "confidence": "High",
            "source": "Google Safe Browsing",
            "daa_reasons": []
        })
    elif is_malicious is None:
        print("Safe Browsing failed, falling back to ML & DAA...")

    # Step 2: DAA Heuristic Check
    heuristic_score, reasons = run_daa_analysis(url)
    if heuristic_score >= 2:
        return jsonify({
            "url": url,
            "prediction": "suspicious",
            "confidence": "High",
            "source": "DAA Heuristics",
            "daa_reasons": reasons
        })

    # Step 3: ML Model
    try:
        vectorized_url = vectorizer.transform([url])
        prediction_encoded = model.predict(vectorized_url)[0]
        prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]
    except Exception as e:
        return jsonify({"error": f"ML model error: {str(e)}"})

    return jsonify({
        "url": url,
        "prediction": prediction_label,
        "confidence": "Moderate",
        "source": "ML Model",
        "daa_reasons": reasons
    })
