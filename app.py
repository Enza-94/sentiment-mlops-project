import gradio as gr
import spaces
from inference import predict_sentiment

@spaces.GPU
def classify_sentiment(text):
    result = predict_sentiment(text)
    return {
        "negative": result["negative"],
        "neutral": result["neutral"],
        "positive": result["positive"],
    }


demo = gr.Interface(
    fn=classify_sentiment,
    inputs=gr.Textbox(label="Text To Analyze", placeholder="Write here your sentence..."),
    outputs=gr.Label(label="Sentiment"),
    title="Sentiment Analysis — MachineInnovators Inc.",
    description="This app classifies the sentence as a neutral, positive or negative text!",
)

if __name__ == "__main__":
    demo.launch()