from fastapi import FastAPI
from pydantic import BaseModel # controllo qualità sui dati input e output dell'API
from inference import predict_sentiment
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
import os
import csv
from datetime import datetime

app = FastAPI()
Instrumentator().instrument(app).expose(app)

sentiment_counter = Counter(
    "sentiment_predictions_total",
    "Numero totale di predizioni per classe di sentiment",
    ["sentiment"]
)

def save_prediction(sentiment_label):
    os.makedirs("reports", exist_ok=True)

    file_path = "reports/predictions.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "sentiment_label"])

        writer.writerow([
            datetime.now().isoformat(),
            sentiment_label
        ])




class TextInput(BaseModel):
    text: str



@app.get("/")
def read_root():
    return {"messaggio": "ciao"}


@app.post("/predict")
def predict(payload: TextInput):
    result = predict_sentiment(payload.text)

    sentiment_counter.labels(sentiment=result["label"]).inc()

    save_prediction(result["label"])

    return result