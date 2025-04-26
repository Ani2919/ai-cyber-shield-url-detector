import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
import pickle

# Load datasets
main_df = pd.read_csv("balanced_phishing_dataset.csv")  # your cleaned + balanced data
boost_df = pd.read_csv("benign_boost.csv")  # additional legit URLs

# Combine and shuffle
df = pd.concat([main_df, boost_df], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Features and labels
X_raw = df["url"]
y_raw = df["label"]

# Vectorize URLs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_raw)

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save components
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
pickle.dump(label_encoder, open("label_encoder.pkl", "wb"))

print("✅ Model, Vectorizer, and Label Encoder saved successfully!")