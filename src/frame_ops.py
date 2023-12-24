import cv2
import numpy as np
import pandas as pd

from .extraction import get_extraction_model


def get_color(frame: np.ndarray, color_extraction: dict) -> np.ndarray:
    frame = frame.reshape((frame.shape[0] * frame.shape[1], 3))

    model = get_extraction_model(color_extraction["method"], color_extraction["params"])
    model.fit(frame)

    return model.get_predominant_color()


def smooth(
    frame: np.ndarray, kernel_size: int = 5, method="GaussianBlur"
) -> np.ndarray:
    kernel = (kernel_size, kernel_size)

    if method == "GaussianBlur":
        if kernel_size % 2 == 0:
            raise ValueError("Kernel size for Gaussian Blur must be odd number.")

        frame = cv2.GaussianBlur(frame, kernel, 0)
    elif method == "MedianBlur":
        frame = cv2.medianBlur(frame, kernel_size)
    elif method == "AverageBlur":
        frame = cv2.blur(frame, kernel)
    else:
        raise ValueError(
            "Smooth method must be: GaussianBlur, MedianBlur or AverageBlur"
        )

    return frame
