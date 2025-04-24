from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample training data
urls = ["http://bad.com", "https://safe.org", "http://phishing.co"]
labels = ["malicious", "safe", "malicious"]

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# Vectorize URLs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(urls)

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save files
with open('phishing_url_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("✅ Model and vectorizer saved successfully.")
