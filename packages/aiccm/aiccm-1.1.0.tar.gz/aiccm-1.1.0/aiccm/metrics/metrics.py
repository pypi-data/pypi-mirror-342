import math

import numpy as np

VIEW_LENGTH = 400  # μm
VIEW_PIXEL = 384
CNBD_MIN_LENGTH = 20


def get_view_area_mm2():
    """ 视野面积(mm2) """
    return (VIEW_LENGTH / 1000) ** 2


def pixel_to_mm(num):
    """ 将像素换算成mm2长度 """
    return num * (VIEW_LENGTH / 1000) / VIEW_PIXEL


def get_length(p):
    """ 所有节段长度(像素) """
    return np.sum(s.length for s in p.segments)


def get_nerve_num(p):
    """ 所有神经纤维主干数目 """
    return len(p.nerves)


def get_nerve_branch_num(p):
    """ 所有从神经纤维主干发出的分支的数目 """
    branch_records, branch_count = [], 0
    for nerve in p.nerves:
        for node in [n for n in nerve.nodes if n.class_node == 'branch']:
            branches = [s.index for s in node.neighbors if p.segments[s.index].class_segment == 'branch']
            branches = [si for si in branches if si not in branch_records]
            branches = [si for si in branches if p.segments[si].length > CNBD_MIN_LENGTH]
            branch_count += len(branches)
            branch_records.extend(branches)

    return branch_count

def get_CNFL_(p):
    """ 角膜神经纤维长度（CNFL，mm/mm2）：每平方毫米所有神经纤维长度之和 """
    return pixel_to_mm(get_length(p)) / get_view_area_mm2()


def get_CNFD_(p):
    """ 角膜神经纤维密度（CNFD） 神经总数/ mm2"""
    return get_nerve_num(p) / get_view_area_mm2()


def get_CNBD_(p):
    """ 角膜神经分支密度(CNBD)，主要神经干分支数/mm2 """
    return get_nerve_branch_num(p) / get_view_area_mm2()



