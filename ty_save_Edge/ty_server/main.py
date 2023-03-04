from multiprocessing import Lock,Value,Process
import multiprocessing
import os
import sys
from ctypes import c_char_p
from server.tcpServer import tcpServer

if __name__ == '__main__':
    print(f"sys.argv:{sys.argv} len:{len(sys.argv)}")
    # if len(sys.argv) > 1:
    #     user_id = sys.argv[1]
    # else:
    #     user_id = "00000000"
    # user_dir = os.path.join("data", user_id)
    # if not os.path.exists(user_dir):
    #     os.makedirs(user_dir, mode=0o777)
    multiprocessing.set_start_method('forkserver',force=True)
    tySignal = Value('i',0)
    tyLock = Lock()
    tyserverLock = Lock()

    sever_IP = "0.0.0.0" #当为0.0.0.0的时候作为接入终端
    severcameraPort = 8386          # 绑定相机设备号

    with multiprocessing.Manager() as MG:
        serverFrameDict = multiprocessing.Manager().dict()
        send_str = multiprocessing.Manager().Value(c_char_p,'1111111')
        serverFrameDict['f'] = None

        servercameraProcess = Process(target=tcpServer(),
                                      args=(sever_IP, severcameraPort, serverFrameDict, tyserverLock, send_str))
        servercameraProcess.start()


        servercameraProcess.join()