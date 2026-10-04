from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys

sys.path.append("/opt/airflow")



def collect_data():
    
    print("TweetEval dataset already available locally.")


def evaluate_model():
    from evaluate_model import evaluate
    evaluate()


def retrain_model():
    from minimal_retraining import retrain
    retrain()


with DAG(
    dag_id="sentiment_ml_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@weekly",
    catchup=False,
) as dag:

    collect = PythonOperator(
        task_id="collect_data",
        python_callable=collect_data,
    )

    evaluate_task = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
    )

    retrain_task = PythonOperator(
        task_id="retrain_model",
        python_callable=retrain_model,
    )

    collect >> evaluate_task >> retrain_task