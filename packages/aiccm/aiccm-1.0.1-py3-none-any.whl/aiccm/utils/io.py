import cv2
import numpy as np

import warnings


def load_image(path):
    """ 加载一张图片 """
    with open(path, 'rb') as file:
        file_data = file.read()
        image_array = np.frombuffer(file_data, np.uint8)
        image_raw = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image_raw


def save_image(image, path='result.png'):
    """ 保存一张图片 """
    extend = '.' + path.split('.')[-1]
    retval, buffer = cv2.imencode(extend, image.astype('uint8'))
    with open(path, 'wb') as f:
        f.write(buffer)


def show_image(image):
    """ 展示一张图片 """
    image_show = image.copy().astype('uint8')
    if np.amax(image_show) == 1:
        image_show = image_show * 255
    cv2.imshow('Show', image_show)
    cv2.waitKey(0)


def load_ccm_image(path):
    """ 加载标准化CCM图像 """
    image_raw = load_image(path)
    match image_raw.shape[:2]:
        case 384, 384:
            return image_raw
        case 484, 384:
            return image_raw[:384, :384]
        case _:
            warnings.warn(
                f"读取的CCM图像分辨率不符合预期，应该为384*384或384*484，而此图像{path}为{image_raw.shape[:2]}",
                UserWarning
            )
