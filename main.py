from fastapi import FastAPI
from pydantic import BaseModel # controllo qualità sui dati input e output dell'API
from inference import predict_sentiment
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI()
Instrumentator().instrument(app).expose(app)

sentiment_counter = Counter(
    "sentiment_predictions_total",
    "Numero totale di predizioni per classe di sentiment",
    ["sentiment"]
)


class TextInput(BaseModel):
    text: str



@app.get("/")
def read_root():
    return {"messaggio": "ciao"}


@app.post("/predict")
def predict(payload: TextInput):
    result = predict_sentiment(payload.text)
    sentiment_counter.labels(sentiment=result["label"]).inc()
    return result