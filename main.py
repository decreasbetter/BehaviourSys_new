import os
import cv2
import numpy as np

from config import Config
from system.System import System
from metacheck.meta import Meta

    
if __name__ == "__main__":

    # 初始化
    cfg = Config()
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

        vis_img = np.copy(ori_img)

        for name, meta in meta_info.items():
                for me in meta:
                    cv2.rectangle(vis_img, me.left_top, me.right_bottom, (0, 0, 134), 3, 4)
                    cv2.putText(vis_img, name, me.left_top, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
        cv2.putText(vis_img, "Behaviour State: " + str(meta_check.behaviour_state), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255), 1)
        cv2.putText(vis_img, "Cur State: " + str(meta_check.cur_sate), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255), 1)
        cv2.putText(vis_img, "Operating State: " + str(meta_check.op_ing), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255), 1)

        cv2.imshow("Vis Img", vis_img)