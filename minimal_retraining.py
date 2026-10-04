import torch
from datasets import load_dataset
from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
MODEL_NAME = "/opt/airflow/model"

def retrain(n_samples=50):

    # Dataset
    # dataset = load_dataset("cardiffnlp/tweet_eval", "sentiment")
    dataset = load_from_disk("data/tweet_eval")
    train_set = dataset["train"].select(range(n_samples))

    # Model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    # Optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=5e-5)

    model.train()

    for epoch in range(5):  # numero basso di epoche

        for example in train_set:

            inputs = tokenizer(
                example["text"],
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=128,
            )

            labels = torch.tensor([example["label"]])

            output = model(**inputs, labels=labels)
            loss = output.loss

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        print(f"Epoch {epoch + 1}/5 completed.")

    # Save retrained model
    model.save_pretrained("retrained_model")
    tokenizer.save_pretrained("retrained_model")

    print("Retraining completed.")


if __name__ == "__main__":
    retrain()