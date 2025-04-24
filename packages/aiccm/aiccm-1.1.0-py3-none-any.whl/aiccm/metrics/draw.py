from aiccm.utils.morphology import get_canvas
import cv2
from typing import Literal

DIGITAL_TYPE = Literal['none', 'both', 'segments', 'node']
SHOW_TYPE = Literal['bone', 'body']


def _draw_digit(image, segments=None, nodes=None):
    """ 附加数字 """
    canvas = image.copy()

    if segments is not None:
        for segment in segments:
            cv2.putText(canvas, str(segment.index), segment.center, cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 255, 0), 1,
                        cv2.LINE_AA)

    if nodes is not None:
        for node in nodes:
            cv2.putText(canvas, str(node.index), node.center, cv2.FONT_HERSHEY_SIMPLEX, .3, (255, 255, 0), 1,
                        cv2.LINE_AA)

    return canvas


def draw_digit_image(segments, nodes, image=None):
    """ 创建带数字的神经骨架图 """
    canvas = get_canvas(3) if image is None else image.copy()

    for segment in segments:
        canvas[segment.bone > 0] = (255, 255, 255)
        cv2.putText(canvas, str(segment.index), segment.center, cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 255, 0), 1,
                    cv2.LINE_AA)

    for node in nodes:
        canvas[node.bone > 0] = (0, 0, 255)
        cv2.putText(canvas, str(node.index), node.center, cv2.FONT_HERSHEY_SIMPLEX, .3, (255, 255, 0), 1, cv2.LINE_AA)

    return canvas


def draw_result_image(segments, nodes, image=None, digital: DIGITAL_TYPE = 'none', show: SHOW_TYPE = 'bone'):
    """ 创建用于结果展示的图像，即以原图为背景，红色骨架代表主干，蓝色骨架代表分支，绿色圆点代表分支点，黄色圆点代表端点 """
    canvas = get_canvas(3) if image is None else image.copy()

    for segment in segments:
        if show == 'bone':
            canvas[segment.bone > 0] = (0, 0, 255) if segment.class_segment == 'main' else (255, 0, 0)
        elif show == 'body':
            canvas[segment.body > 0] = (0, 0, 255) if segment.class_segment == 'main' else (255, 0, 0)

    for node in nodes:
        if show == 'bone' and node.class_node == 'branch':
            cv2.circle(canvas, node.center, 2, (0, 255, 0), -1)
        elif show == 'body' and node.class_node == 'branch':
            cv2.circle(canvas, node.center, 4, (0, 255, 0), -1)


    if digital == 'both':
        params = (segments, nodes)
    elif digital == 'segments':
        params = (segments,)
    elif digital == 'nodes':
        params = (nodes,)
    else:
        params = ()

    canvas = _draw_digit(canvas, *params)

    return canvas


def draw_trunk_image(segments, image=None):
    """ 创建仅标注主干的图像 """
    canvas = get_canvas(3) if image is None else image.copy()
    for segment in [s for s in segments if s.class_segment == 'main']:
        canvas[segment.bone > 0] = (0, 0, 255)

    return canvas
