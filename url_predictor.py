import pickle

# Load components
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

# Prediction loop
while True:
    url = input("🔗 Enter a URL to test (or type 'exit'): ").strip()
    if url.lower() == "exit":
        break
    vec_url = vectorizer.transform([url])
    pred = model.predict(vec_url)
    label = label_encoder.inverse_transform(pred)[0]
    print(f"🛡️ Prediction: {label}\n")