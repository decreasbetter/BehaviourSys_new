import os
import cv2
import numpy as np

from config import Config as cfg
from system.System import System
from metacheck.meta import Meta

    
if __name__ == "__main__":

    # 初始化
    Sys = System(cfg)

    # 加载模型
    model = Sys.model

    # 加载视频
    camera = Sys.camera

    # 加载基元检测器
    meta_check = Meta(cfg)

    while True:

        # 读取视频帧
        success, ori_img = camera.cap.read()
        if not success:
            print('Waiting for the video input.\n')
            continue

        input_img = np.copy(ori_img)
        meta_info = model(input_img)

        meta_check.update(meta_info)