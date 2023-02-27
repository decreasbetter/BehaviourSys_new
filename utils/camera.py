import cv2


class Camera():

    def __init__(self, cfg) -> None:
        
        cap = cv2.VideoCapture(cfg.vidoe_capture)  #生成读取摄像头对象
        
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')    #视频的编码
        cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.img_w)  #设置视频的宽度
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.img_h)  #设置视频的高度
        cap.set(cv2.CAP_PROP_FPS, cfg.fps)

        self.cap = cap
        

            