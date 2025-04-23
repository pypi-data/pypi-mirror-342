from .processor import Processor
from .metrics import get_CNFL_, get_CNFD_, get_CNBD_
from .draw import draw_result_image

import numpy as np

p = Processor()


def get_CNFL(image: np.ndarray) -> float:
    p.load_image(image)
    p.process(trunk_rec=False)
    return round(get_CNFL_(p), 4)

def get_CNFD(image: np.ndarray) -> float:
    p.load_image(image)
    p.process(trunk_rec=True)
    return round(get_CNFD_(p), 4)

def get_CNBD(image: np.ndarray) -> float:
    p.load_image(image)
    p.process(trunk_rec=True)
    return round(get_CNBD_(p), 4)

def get_metrics(image: np.ndarray) -> dict[str, float]:
    p.load_image(image)
    p.process(trunk_rec=True)
    return {
        'CNFL': round(get_CNFL_(p), 4),
        'CNFD': round(get_CNFD_(p), 4),
        'CNBD': round(get_CNBD_(p), 4),
    }

def get_bone_image(image: np.ndarray | None = None) -> np.ndarray:
    return draw_result_image(
        p.segments, p.nodes, image=image, show='bone'
    )

def get_body_image(image: np.ndarray | None = None) -> np.ndarray:
    return draw_result_image(
        p.segments, p.nodes, image=image, show='body'
    )

