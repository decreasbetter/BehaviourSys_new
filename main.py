import os
import cv2
import numpy as np

from config import Config as cfg
from utils.camera import Camera
from models.model import 


    
if __name__ == "__main__":

    # 加载配置

    # 捕获摄像头
    cap = Camera(cfg)

    # 加载模型
    model = 

    while True:

        # 读取视频帧
        success, ori_img = cap.read()
        if not success:
            print('Waiting for the video input.\n')
            continue
