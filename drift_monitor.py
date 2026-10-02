import pandas as pd
from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset


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

    reference = pd.DataFrame({
        "sentiment_label": ["positive"] * 60 + ["neutral"] * 30 + ["negative"] * 10
    })
     # Leggiamo le predizioni reali generate dall'API
    predictions_file = "reports/predictions.csv"

    current = pd.read_csv(predictions_file)

    current = current[["sentiment_label"]]


    negative_ratio = (
    (current["sentiment_label"] == "negative").sum()
    / len(current))

    print(f"Negative sentiment: {negative_ratio:.1%}")

    if negative_ratio > 0.30:
        print("REPUTATION ALERT: ON")
    else:
        print("REPUTATION ALERT: OFF")

    # Generiamo il report
    evaluation = build_drift_report(
        reference,
        current,
        output_path="reports/drift_report.html"
    )

    print("Report generato: reports/drift_report.html")
   