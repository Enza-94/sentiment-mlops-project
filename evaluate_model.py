from datasets import load_from_disk
from inference import predict_sentiment

LABEL_MAP = {"negative": 0, "neutral": 1, "positive": 2} # il modello ha come output 1,2,3; a noi restituisce negative, neutral, positive; perciò bisogna fare un mapping


def evaluate(n_samples = 500):
    dataset = load_from_disk("data/tweet_eval")
    test_set = dataset["test"].select(range(n_samples))

    correct = 0
    for example in test_set:
        result = predict_sentiment(example["text"]) # il dataset ha due colonne, una text (con la frase) e una label (neutrale, positivo, negativo)
        
        predicted_label = LABEL_MAP[result["label"]]
        if predicted_label == example["label"]:
            correct += 1

    accuracy = correct / len(test_set)
    print(f"Accuracy on {len(test_set)} examples: {accuracy:.2%}")
    return accuracy


if __name__ == "__main__":
    evaluate()