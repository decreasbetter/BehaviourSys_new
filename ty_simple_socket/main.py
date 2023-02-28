from multiprocessing import Lock,Value,Process,Queue
import multiprocessing
import time
from ClientCamera import client_camera
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = 'TRUE'

if __name__ == '__main__':
    multiprocessing.set_start_method('forkserver', force=True)
    IP = "0.0.0.0"     #服务器IP
    severcameraPort = 8386          # 绑定相机设备号
    camera_name = "/dev/camera_ty"
    tySignal = Value('i',0)
    tyLock = Lock()
    tyserverLock = Lock()

    with multiprocessing.Manager() as MG:
        serverFrameDict = multiprocessing.Manager().dict()
        serverFrameDict['s'] = None

        cameraProcess = Process(target=client_camera,
                                args=(IP, severcameraPort, camera_name, tyLock, serverFrameDict))
        cameraProcess.start()

        cameraProcess.join()

