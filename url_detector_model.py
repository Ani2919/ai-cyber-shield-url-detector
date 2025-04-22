from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle

# Load your cleaned dataset with proper encoding
df = pd.read_csv('cleaned_malicious_phish.csv', encoding='ISO-8859-1')
df = df[['url', 'label']].dropna()

# Replace NaN URLs with empty strings
df['url'] = df['url'].fillna('')

X = df['url']
y = df['label']

# Convert labels from string to numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# TF-IDF Vectorizer with reduced features to prevent memory error
vectorizer = TfidfVectorizer(max_features=10000)  
X_vectorized = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y_encoded, test_size=0.2, random_state=42
)

# Memory-optimized XGBoost model
model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method='hist',
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the trained model as .pkl
with open('phishing_url_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model saved successfully as phishing_url_model.pkl!")
# Save vectorizer too!
with open('tfidf_vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

print("✅ Vectorizer saved successfully as tfidf_vectorizer.pkl!")
with open('label_encoder.pkl', 'wb') as le_file:
    pickle.dump(label_encoder, le_file)

print("✅ Label encoder saved as label_encoder.pkl!")
