import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


DATA_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/training_data.csv"
MODEL_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/ranker.pkl"


df = pd.read_csv(DATA_FILE)


body_encoder = LabelEncoder()
priority_encoder = LabelEncoder()


df["body_type"] = body_encoder.fit_transform(df["body_type"])
df["priority"] = priority_encoder.fit_transform(df["priority"])


X = df.drop("chosen", axis=1)
y = df["chosen"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model accuracy:", accuracy)


joblib.dump(
    {
        "model": model,
        "body_encoder": body_encoder,
        "priority_encoder": priority_encoder
    },
    MODEL_FILE
)

print("Model saved.")