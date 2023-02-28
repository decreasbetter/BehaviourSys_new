import os


class Config():
    """
    功能: 
    """

    def __init__(self) -> None:
        
        self.meta = ['hand', 'hand', 'fin', 'sticker']  # 基元
        self.spatial_relation = ['hand-fin-concate', 'hand-hand-concate', 'hand-hand-depart', 'fin-sticker-depart']  # 基元间的空间交互规则，包括"交互"、"分离"
        self.temporal_relation = [[0], [1], [2, 3]]  # 基元间空间交互发生的时间顺序, 出现两个表示或关系

        self.model_type = 'yolov5'
        self.model_path = 'model\yoloV5\weights\\best_3.pt'  # 检测模型权重路径
        self.input_shape = [640, 480]  # 模型输入大小
        
        if self.model_type == 'yolov5':
            self.data_ymal = 'model\yoloV5\hand.yaml'  # 模型检测类别与类别数目
            self.conf_thres = 0.5  # 预测置信度阈值
            self.iou_thres = 0.5  # nms时的iou阈值
        else:
            self.class_name = []
            

        self.save_path = 'outputdata'  # 错误数据存储路径
        
        self.vidoe_capture = 'F:\LIUYI\研究生\学校项目\代码\\2022-12-05-09-06-33_hs2.avi'  #摄像头设备号路径    
        self.img_w = 1280
        self.img_h = 720
        self.fps = 60
