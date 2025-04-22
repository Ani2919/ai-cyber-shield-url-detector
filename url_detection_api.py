from flask import Flask, request, jsonify
import pickle

# Load trained model, vectorizer, and label encoder
with open('phishing_url_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_url():
    data = request.json
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Vectorize the input URL
    vector = vectorizer.transform([url])

    # Predict using the trained model
    prediction = model.predict(vector)[0]

    # Decode the predicted label
    label = label_encoder.inverse_transform([prediction])[0]

    return jsonify({'prediction': label})

if __name__ == '__main__':
    app.run(debug=True)
