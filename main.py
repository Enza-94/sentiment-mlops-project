from fastapi import FastAPI
from pydantic import BaseModel # controllo qualità sui dati input e output dell'API
from inference import predict_sentiment
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)


class TextInput(BaseModel):
    text: str



@app.get("/")
def read_root():
    return {"messaggio": "ciao"}


@app.post("/predict")
def predict(payload: TextInput):
    return predict_sentiment(payload.text)