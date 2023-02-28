import os
import numpy as np


def checkDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


class objInfo():
    """
    功能: 完成基元之间的空间交互信息判断
    输入: 基元检测结果, 如目标框坐标、置信度
    return: objInfo class
    """

    def __init__(self, obj: list) -> None:
        self.score = obj[4]
        left_top_x, left_top_y, right_bottom_x, right_bottom_y = obj[:4]
        self.left_top = np.array([left_top_x, left_top_y])  # 目标框的左上角坐标
        self.right_bottom = np.array([right_bottom_x, right_bottom_y])  # 目标框的右下角坐标
        self.center = (self.left_top + self.right_bottom) / 2  #目标框中心坐标


    def isConcate(self, other, thresh=0.1):
        
        return self.getIou(other) >= thresh

    def isDepart(self, other):

        if not self.isConcate(other, 0.05):
            return True
        return False


    def getIou(self, other):

        box1 = [self.left_top[1], self.left_top[0], self.right_bottom[1], self.right_bottom[0]]
        box2 = [other.left_top[1], other.left_top[0], other.right_bottom[1], other.right_bottom[0]]
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

        sum_area =area1 + area2

        left_line = max(box1[1], box2[1])
        right_line = max(box1[3], box2[3])
        top_line = max(box1[0], box2[0])
        bottom_line = max(box1[2], box2[2])

        if left_line >= right_line or top_line >= bottom_line:
            return False
        else:
            intersect = (right_line - left_line) * (bottom_line - top_line)
            return (intersect / (sum_area - intersect)) * 1.0