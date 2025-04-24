from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle

# ✅ Load dataset
df = pd.read_csv('cleaned_malicious_phish.csv', encoding='ISO-8859-1')
df = df[['url', 'label']].dropna()
df['url'] = df['url'].fillna('')

# ✅ Labels & features
X = df['url']
y = df['label']

# ✅ Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ✅ TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=10000)
X_vectorized = vectorizer.fit_transform(X)

# ✅ Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y_encoded, test_size=0.2, random_state=42
)

# ✅ Train XGBoost model
model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method='hist',
    random_state=42
)
model.fit(X_train, y_train)

# ✅ Evaluate
y_pred = model.predict(X_test)
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))

# ✅ Save model
with open('phishing_url_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# ✅ Save vectorizer
with open('tfidf_vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

# ✅ Save label encoder
with open('label_encoder.pkl', 'wb') as le_file:
    pickle.dump(label_encoder, le_file)

print("✅ All files saved successfully!")
