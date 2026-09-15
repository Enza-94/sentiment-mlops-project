# 1st step: creation of the virtual enviroment

conda create --name sentiment-env python=3.11
python -m ipykernel install --user --name sentiment-env --display-name "Python (sentiment-env)

uvicorn main:app --reload # per lanciare il server 

inference.py --> ROBERTA sentiment analysis

http://127.0.0.1:8000/docs#/default/predict_predict_post




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

set HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx

set HF_REPO_ID=Enza-94/sentiment-mlops-app