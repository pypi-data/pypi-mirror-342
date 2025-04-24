from aiccm.utils.io import load_ccm_image
from aiccm.segment.detector import segmenter
from aiccm.utils.morphology import skeletonize_, split

from .point import get_points
from .instance import get_instance
from .graph import get_trunk
from .concat import get_nerve
from .draw import draw_result_image


class Processor:
    def __init__(self):
        self.image = None
        self.images = {
            'binary': None,
            'result': None,
        }

        self.model_path = None

        self.segments = []
        self.nodes = []
        self.nerves = []



    def load_image(self, image):
        self.image = image.copy()
        self.segments = []
        self.nodes = []
        self.nerves = []

    def process(self, trunk_rec=True):
        binary = segmenter(self.image)
        self.images['binary'] = binary
        skeleton = skeletonize_(binary)
        blocks, _ = split(skeleton, split_skeleton=True)
        for block in blocks:
            points, end_points = get_points(block)
            instance = get_instance(binary, block, points, end_points)
            segments, nodes = instance
            self.segments.extend(segments)
            self.nodes.extend(nodes)

            if trunk_rec:
                trunks = get_trunk(*instance)
                if trunks:
                    for sis, nis in trunks:
                        for si in sis:
                            segments[si].class_segment = 'main'
                        self.nerves.append(get_nerve([segments[si] for si in sis], [nodes[ni] for ni in nis]))

        # 重新编号
        for i, segment in enumerate(self.segments):
            segment.index = i

        for i, node in enumerate(self.nodes):
            node.index = i

        self.images['result'] = draw_result_image(self.segments, self.nodes, self.image)




