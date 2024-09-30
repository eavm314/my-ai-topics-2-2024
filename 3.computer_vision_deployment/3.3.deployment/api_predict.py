import io
import csv
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
import numpy as np
from PIL import Image, UnidentifiedImageError

from predict import predict_image
from model import *

app = FastAPI(title="Prediction API")

@app.post("/predict")
def predict_image_endpoint(file: UploadFile = File(...)):
    # crear byte stream
    img_stream = io.BytesIO(file.file.read())
    # convertir a una imagen de Pillow
    try:
        img_obj = Image.open(img_stream)
    except UnidentifiedImageError as e:
        raise HTTPException(status_code=415, detail=f"not supported: {e}")
    # crear array de numpy
    img_array = np.array(img_obj)
    shape = Shape(width=img_array.shape[1], height=img_array.shape[0], channels=img_array.shape[2])
    print(shape)
    name, conf = predict_image(img_array)
    prediction = Prediction(class_name=name, confidence=conf)
    response = FilePrediction(filename=file.filename, image_size=file.size, image_shape=shape, prediction=prediction)
    
    return response

@app.post("/annotate")
def annotate(file: UploadFile = File(...)):
    img_stream = io.BytesIO(file.file.read())
    img_obj = Image.open(img_stream)
    img_array = np.array(img_obj)
    name, conf = predict_image(img_array)

    image_text = cv2.putText(img_array, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    _, encoded_image = cv2.imencode('.jpeg', image_text)
    stream = io.BytesIO(encoded_image.tobytes())
    
    return StreamingResponse(stream, media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_predict:app", reload=True)