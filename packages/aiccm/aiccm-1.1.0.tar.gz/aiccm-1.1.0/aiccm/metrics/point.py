import numpy as np
import cv2


from aiccm.utils.morphology import skeletonize_, get_canvas, dilated, split



END_KERNEL = np.array([[1, 1, 1],
                       [1, 10, 1],
                       [1, 1, 1]])



def get_points(skeleton):
    """ 查找骨架图中的分支点 """
    neighbors = cv2.filter2D((skeleton > 0).astype('uint8'), -1, END_KERNEL)
    nodes_mask = neighbors >= 13
    ends_mask = neighbors == 11

    skeleton2 = skeleton.copy()
    skeleton2[nodes_mask] = 0

    segments, _ = split(skeleton2, True)

    for segment in segments:
        if cv2.countNonZero(segment) < 4 and cv2.countNonZero(
                cv2.bitwise_and(segment, (ends_mask * 255).astype('uint8'))):
            skeleton[segment > 0] = 0

    skeleton = skeletonize_(skeleton, min_area=-1)

    neighbors = cv2.filter2D((skeleton > 0).astype('uint8'), -1, END_KERNEL)
    nodes_mask = neighbors >= 13
    ends_mask = neighbors == 11

    points = get_canvas()
    points[nodes_mask] = 255
    points = dilated(points, iteration=3)
    points = cv2.bitwise_and(points, skeleton)

    end_points = get_canvas()
    end_points[ends_mask] = 255

    return points, end_points

