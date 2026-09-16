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
    reference = pd.DataFrame({
        "sentiment_label": ["positive"] * 60 + ["neutral"] * 30 + ["negative"] * 10
    })
    current = pd.DataFrame({
        "sentiment_label": ["positive"] * 40 + ["neutral"] * 30 + ["negative"] * 30
    })

    build_drift_report(reference, current)
    print("Report generato: drift_report.html")