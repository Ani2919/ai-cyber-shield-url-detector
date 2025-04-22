import pickle

# Load trained model
with open('phishing_url_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load TF-IDF vectorizer
with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Load label encoder
with open('label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

# Predict function
def predict_url(url):
    url_vector = vectorizer.transform([url])
    prediction = model.predict(url_vector)[0]
    label = label_encoder.inverse_transform([prediction])[0]
    return label

# Real-time user input
while True:
    url_input = input("🔗 Enter a URL to check (or type 'exit' to quit): ")
    if url_input.lower() == 'exit':
        break
    result = predict_url(url_input)
    print(f"🚨 The URL is predicted to be: **{result.upper()}**\n")
