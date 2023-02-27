import os
import numpy as np


def checkDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


class objInfo():
    """
    功能: 完成基元之间的空间交互信息判断
    输入: 基元检测结果, 如目标框坐标、置信度
    """

    def __init__(self, obj: list) -> None:
        self.score = obj[5]
        left_top_x, left_top_y, right_bottom_x, right_bottom_y = obj[:4]
        self.left_top = np.array([left_top_x, left_top_y])  # 目标框的左上角坐标
        self.right_bottom = np.array([right_bottom_x, right_bottom_y])  # 目标框的右下角坐标
        self.center = (self.left_top + self.right_bottom) / 2  #目标框中心坐标


    def isConcate(self):
        pass

    def isDepart(self):
        pass