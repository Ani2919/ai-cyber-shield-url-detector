from flask import Flask, request, jsonify
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the saved model and preprocessing tools
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

@app.route('/', methods=['GET'])
def home():
    return "🚀 Welcome to Anika's AI Cyber Shield API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({"error": "URL missing in request"}), 400

    url = data['url']

    # Preprocess and predict
    vectorized_url = vectorizer.transform([url])
    prediction_encoded = model.predict(vectorized_url)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

    return jsonify({
        "url": url,
        "prediction": prediction_label
    })

if __name__ == '__main__':
    app.run(debug=True)
