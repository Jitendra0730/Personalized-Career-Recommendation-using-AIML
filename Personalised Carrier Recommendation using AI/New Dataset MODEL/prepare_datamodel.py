import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
data = pd.read_csv(r"C:/Users/metro/Desktop/UDP 7th Sem/Personalised Carrier Recommendation using AI/New Dataset MODEL/New Dataset/job_recommendation_dataset.csv")

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create job descriptions
job_texts = data['Job Title'] + " " + data['Industry'] + " " + data['Required Skills']

# Compute embeddings once
job_embeddings = model.encode(job_texts.tolist(), show_progress_bar=True)

# Save embeddings
np.save("job_embeddings.npy", job_embeddings)

# ---- Optional: Train RandomForest only once ----
X = job_embeddings
y = data["Industry"]  # or any label column you want to predict
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save trained model
joblib.dump(clf, "predicting_model.pkl")

print("Preprocessing complete. Embeddings + Model saved.")
