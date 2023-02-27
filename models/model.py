import torch
import numpy as np
from collections import defaultdict

from utils.util import objBBox
from yoloV5.models.common import DetectMultiBackend
from yoloV5.utils.augmentations import letterbox
from yoloV5.utils.general import non_max_suppression, scale_coords


"""
功能: 该模块主要进行基元检测
输入: 视频帧图像
输出: 基元检测结果, 主要为手部姿态或目标检测框
"""



def make_model(cfg):
    if cfg.model.lower() == 'yolov5':
        from yoloV5.utils.torch_utils import select_device
        device = select_device()
        model = Yolov5(cfg, device)

    
    return model


class Yolov5(DetectMultiBackend):

    def __init__(self, cfg, device=torch.device('cpu')):
        super().__init__(weights=cfg.model_path, device=device, data=cfg.data_ymal)
        self.device = device
        self.input_shape = cfg.input_shape
        self.conf_thres = cfg.conf_thres
        self.iou_thres = cfg.iou_thres
        self.ori_imgshape = np.array([cfg.img_w, cfg.img_h])
        
    def preProcess(self, frame):

        img = np.copy(frame)
        # Padded resize
        img = letterbox(img, self.input_shape, stride=self.stride, auto=self.pt)[0]
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.fp16 else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        return img

    
    def forward(self, im, augment=False, visualize=False, val=False):
        im = self.preProcess(im)
        pre = super().forward(im, augment, visualize, val)
        pre = self.postProcess(pre)
        return pre

    def postProcess(self, pre):
        # pre: shape->[n, 6], n个目标, 每个目标[x_left-top, y_left-top, x_right-bottom, y_right-bottom, confi, cls]
        pre = non_max_suppression(pre, conf_thres=self.conf_thres, iou_thres=self.iou_thres)
        
        meta_object = defaultdict(list)
        if len(pre):
            pre[:, :4] = scale_coords(self.input_shape, pre[:, :4], self.ori_imgshape).round()
            pre = np.array(pre.to('cpu'))

            # 基元归类
            for obj in pre:
                cls = int(obj[5])  # 目标类别
                obj_info = objBBox(obj[:4].astype(int))  # 目标框

                meta_object[self.name[cls]].append(obj_info)
        return meta_object