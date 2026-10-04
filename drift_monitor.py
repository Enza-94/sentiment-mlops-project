import pandas as pd
from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset
from prometheus_client import Gauge
from prometheus_client import start_http_server
import os
import time



negative_sentiment_ratio = Gauge(
    "negative_sentiment_ratio",
    "Percentuale di predizioni con sentiment negativo"
)

reputation_alert = Gauge(
    "reputation_alert",
    "Alert reputazionale: 1 se il sentiment negativo supera il 30%, 0 altrimenti"
)


def build_drift_report(reference_df, current_df, output_path: str = "drift_report.html"):
    definition = DataDefinition(categorical_columns=["sentiment_label"])

    reference_dataset = Dataset.from_pandas(reference_df, data_definition=definition)
    current_dataset = Dataset.from_pandas(current_df, data_definition=definition)

    report = Report([DataDriftPreset()])
    evaluation = report.run(current_dataset, reference_dataset)
    evaluation.save_html(output_path)
    return evaluation

if __name__ == "__main__":

    import os
    os.makedirs("reports", exist_ok=True)

    start_http_server(8001)

    reference = pd.DataFrame({
        "sentiment_label": ["positive"] * 60 +
                           ["neutral"] * 30 +
                           ["negative"] * 10
    })

    while True: 
        # calcola ogni 60 secondi negative_ratio, aggiorna le metriche e genera il report

        predictions_file = "reports/predictions.csv"

        current = pd.read_csv(predictions_file)
        current = current[["sentiment_label"]]

        recent = current.tail(20) # prendo solo le ultime 20 predizioni

        if len(recent) >= 20:

            negative_ratio = (
                (current["sentiment_label"] == "negative").sum()
                / len(current)
            )

            negative_sentiment_ratio.set(negative_ratio)

            if negative_ratio > 0.30:
                reputation_alert.set(1)
                print("REPUTATION ALERT: ON")
            else:
                reputation_alert.set(0)
                print("REPUTATION ALERT: OFF")

            print(f"Negative sentiment: {negative_ratio:.1%}")

        else:

            negative_sentiment_ratio.set(0)
            reputation_alert.set(0)
            print(f"Not enough predictions for reputation monitoring: "f"{len(recent)}/20")
        
        # evidently drift_monitoring, uses all available predictions

        evaluation = build_drift_report(
            reference,
            current,
            output_path="reports/drift_report.html"
        )

        print("Report generato: reports/drift_report.html")

        time.sleep(60)
   