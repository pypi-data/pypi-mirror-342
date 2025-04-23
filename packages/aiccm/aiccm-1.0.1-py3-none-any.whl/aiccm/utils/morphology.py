import cv2
import numpy as np
from scipy.ndimage import label
import math
from skimage.morphology import skeletonize


# 常量
CANVAS_SHAPE = (384, 384)
DILATED_KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
CLOSE_KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
STRUCTURE_4 = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]])

STRUCTURE_8 = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])


def get_canvas(channels=1):
    """ 获取一张空画布图像 """
    if channels > 1:
        return np.zeros([*CANVAS_SHAPE, channels], dtype='uint8')
    return np.zeros(CANVAS_SHAPE, dtype='uint8')


def dilated(image, kernel=None, iteration=1):
    """ 膨胀运算 """
    dilated_image = cv2.dilate(image, DILATED_KERNEL if kernel is None else kernel, iterations=iteration)
    return dilated_image


def close(image, kernel=None, iteration=1):
    """ 闭运算 """
    closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel=CLOSE_KERNEL if kernel is None else kernel,
                                    iterations=iteration)
    return closed_image


def distance(p1, p2):
    """ 计算欧氏距离 """
    p1, p2 = np.array(p1), np.array(p2)
    return np.linalg.norm(p1 - p2)


def split(image, split_skeleton=False):
    """ 分割连通性区域 """
    image = image > 0
    if not split_skeleton:
        arrays, num = label(image, structure=STRUCTURE_4)
    else:
        arrays, num = label(image, structure=STRUCTURE_8)

    segments = []
    for i in range(1, num + 1):
        component_image = np.where(arrays == i, 1, 0)
        component_image = component_image * 255
        component_image = component_image.astype('uint8')
        segments.append(component_image)

    return segments, num


def calculate_angle(p1, p2, p3):
    """ 计算近似曲线的拐角 """
    v1 = p1 - p2
    v2 = p3 - p2
    try:
        angle = math.degrees(math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
    except ValueError:
        angle = 180
    return angle


def skeletonize_(image, min_area=8):
    """ 将图片骨架化 """
    image = image > 0
    skeleton = skeletonize(image)
    skeleton = skeleton.astype('uint8')
    skeleton = skeleton * 255

    # 设置边缘像素为0
    skeleton[0, :] = 0  # 上边缘
    skeleton[-1, :] = 0  # 下边缘
    skeleton[:, 0] = 0  # 左边缘
    skeleton[:, -1] = 0  # 右边缘

    # 过滤噪点
    if min_area > 0:
        segments, _ = split(skeleton, True)

        for segment in segments:
            if cv2.countNonZero(segment) < min_area:
                skeleton[segment > 0] = 0

    return skeleton
