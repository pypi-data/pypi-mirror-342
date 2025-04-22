from .onnx.detector import NerveSegmenter
from .utils.skeleton import skeletonize_

import os
import numpy as np

here = os.path.abspath(os.path.dirname(__file__))

segmenter = NerveSegmenter(os.path.join(here, 'models/nerve.onnx'))


def get_binary(image: np.ndarray) -> np.ndarray:
    return segmenter(image)


def get_skeleton(image: np.ndarray) -> np.ndarray:
    return skeletonize_(image)
