
from model.model import make_model
from utils.camera import Camera
from utils.util import checkDir


class System(object):

    def __init__(self, cfg) -> None:
        
        self.model = make_model(cfg)  # 创建并加载检测模型
        self.camera = Camera(cfg)  # 初始化摄像头
        
        self.save_path = cfg.save_path  # 错误视频报错路径
        checkDir(self.save_path)