from .utils.morphology import skeletonize_
from .segment.detector import segmenter

import numpy as np


def get_binary(image: np.ndarray) -> np.ndarray:
    return segmenter(image)


def get_skeleton(image: np.ndarray) -> np.ndarray:
    return skeletonize_(image)
