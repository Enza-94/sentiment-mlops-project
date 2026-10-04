from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoConfig
import torch
import numpy as np
from scipy.special import softmax

# MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
MODEL_NAME = "/opt/airflow/model"

# modificato da: https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
config = AutoConfig.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)


def predict_sentiment(text:str)-> dict:
    
    encoded_input = tokenizer(text, return_tensors='pt')
    
    with torch.no_grad():
        output = model(**encoded_input)
        
    scores = softmax(output[0][0].detach().numpy())

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    
    result = {}
    
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        result[l] = float(np.round(s, 4))
    
    result["label"] = config.id2label[ranking[0]]

    return result



if __name__ == "__main__":
    examples = [
        "Adoro questo prodotto, funziona benissimo!",
        "Il servizio clienti mi ha lasciato molto deluso.",
        "Ho ricevuto il pacco ieri.",
    ]
    for text in examples:
        print(text, "->", predict_sentiment(text))