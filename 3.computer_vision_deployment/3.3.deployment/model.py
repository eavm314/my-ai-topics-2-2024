import json
from enum import Enum

from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class Shape(BaseModel):
    width: int
    height: int
    channels: int

class Prediction(BaseModel):
    class_name: str
    confidence: float

class FilePrediction(BaseModel):
    """
    This is the description of the main model
    """

    model_config = ConfigDict(title='Main')

    filename: str
    image_size: int
    image_shape: Shape
    prediction: Prediction