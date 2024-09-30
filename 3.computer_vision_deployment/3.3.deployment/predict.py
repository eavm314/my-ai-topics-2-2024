import os
import numpy as np
from ultralytics import YOLO

def predict_image(image):
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    model_dir = os.path.join(curr_dir, f"models/best.pt")

    print(f"model directory: {model_dir}")

    model = YOLO(model_dir)

    results = model(image)

    prediction = results[0]

    print(prediction.names)
    print(prediction.probs)

    return prediction.names[prediction.probs.top1], prediction.probs.top1conf.item()