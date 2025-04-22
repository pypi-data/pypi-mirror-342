from skimage.morphology import skeletonize
from scipy.ndimage import label

import cv2
import numpy as np

STRUCTURE_4 = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]])

STRUCTURE_8 = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])


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
