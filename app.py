from flask import Flask, request, jsonify
import pickle
import traceback

app = Flask(__name__)

try:
    with open('phishing_url_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print("✅ All files loaded successfully!")
except Exception as e:
    print("❌ Error loading model files:")
    print(traceback.format_exc())

@app.route('/')
def home():
    return "<h1>AI Cyber Shield API is Running!</h1><p>Use POST /predict with JSON to test URLs.</p>"

@app.route('/predict', methods=['POST'])
def predict_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        vector = vectorizer.transform([url])
        prediction = model.predict(vector)[0]
        label = label_encoder.inverse_transform([prediction])[0]

        return jsonify({'prediction': label})
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed.',
            'details': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
