from PIL import Image
import os
from ultralytics import YOLO
import torch
import gc

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'weights/best_cls.pt')


def getModel():
    model = YOLO(model_path)
    # Load model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    model.to(device)
    return model


def examine(model, imgFile):
    class_names = ['IllegibleMeter', 'Calculator', 'Meter', 'Non-Meter']

    # Load image
    img = Image.open(imgFile)

    # Run prediction on GPU
    results = model(img, verbose=False)

    pred = results[0].probs.top1
    confidence = results[0].probs.top1conf.item()

    gc.collect()
    torch.cuda.empty_cache()
    return class_names[pred]