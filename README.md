**Sentiment Analysis MLOps Project**

This project implements a simple MLOps pipeline for sentiment analysis, integrating model serving, monitoring, visualization, and workflow orchestration.

**PROJECT OVERVIEW**

The project combines:

- FastAPI – exposes the sentiment analysis model through an API
- Prometheus – collects prediction metrics
- Grafana – visualizes model and prediction metrics (in particular the sentiment distribution and the reputation alert)
- Airflow – orchestrates the ML workflow
- Docker – runs the different services in a reproducible environment

The model classifies text into three sentiment categories:

    - Positive
    - Neutral
    - Negative

**HOW TO RUN:**

Clone the repository:

git clone https://github.com/Enza-94/sentiment-mlops-project.git

cd sentiment-mlops-project

Start the services with Docker Compose:

docker compose up

The main services can then be accessed through their configured local ports.


For a short description of the architecture, workflow, monitoring, and results, see:

**DOCUMENTATION.md**

MAIN RESULTS

The complete pipeline was tested with sentiment predictions and monitoring through Prometheus and Grafana.

The monitoring dashboard allows the distribution of sentiment predictions and other relevant metrics to be observed during execution, like the reputation alert. 
Reputation alert 

**TECHNOLOGIES**

Python · FastAPI · Docker · Prometheus · Grafana · Airflow · GitHub
