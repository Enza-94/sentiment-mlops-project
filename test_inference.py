from inference import predict_sentiment

def test_positive_sentiment():
    result = predict_sentiment("I love this product, it works very well!")
    assert result["label"] == "positive"

def test_negative_sentiment():
    result = predict_sentiment("This is the worst delivery service I've ever experienced.")
    assert result["label"] == "negative"

def test_neutral_sentiment():
    result = predict_sentiment("The package was delivered yesterday.")
    assert result["label"] == "neutral"

def test_probabilities_sum_to_one():
    result = predict_sentiment("Some random text")
    total = result["negative"] + result["neutral"] + result["positive"]
    assert abs(total - 1.0) < 0.001