import socket
import cv2
import numpy
import time
import pickle
import sys
import copy


class SocketBind:
    def __init__(self, ip='127.0.0.1', port=8002):
        self.address = (ip, port)
        print(self.address)
        self.bind()
        # self.reconnect()
        self.count = 0
        self.counts = 0
        ret = self.connect()
        if ret == False:
            print("connect false")

    def reconnect(self):
        if self.count > 100:
            return False
        if self.counts % 5 == 0:
            if self.connect():
                return True
            else:
                self.count += 1
                time.sleep(self.counts * 10 + 1)
                self.reconnect()

        return False

    def connect(self):
        # 开启连接
        try:
            self.sock.connect(self.address)
            return True
        except socket.error as msg:
            # print(msg)
            return False

    def bind(self):
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def send(self, streamData):
        # 先发送要发送的数据的长度
        # ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
        self.sock.send(str.encode(str(len(streamData)).ljust(16)))
        # 发送数据
        self.sock.send(streamData)

    def recvall(self, sock, count):
        buf = b''  # buf是一个byte类型
        while count:
            # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def receive(self):
        length = self.recvall(self.sock, 16)  # 获得图片文件的长度,16代表获取长度
        getinfo = self.recvall(self.sock, int(length))  # 根据获得的文件长度，获取图片文件
        res = pickle.loads(getinfo)
        return res  # 将数组解码成图像


    def close(self):
        self.sock.close()


class MyCameraSend:
    def __init__(self, camera_name=0, image_good=100):
        """摄像头id 图像质量"""
        # 初始化摄像头

        self.cap = cv2.VideoCapture(camera_name)
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        # fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))    #视频的编码
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        for i in range(2):  # 建立图像读取对象, 先读取一帧（因为有些摄像头开始的几帧比较慢）
            self.cap.read()
        # 压缩参数，后面cv2.imencode将会用到，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), image_good]
        print("Mycamera init end!")

    def read(self):
        ret, frame = self.cap.read()
        # print(f"frame: [{frame}]")
        frame = cv2.resize(frame, (1280, 720))
        if not ret:
            print("not capture camera!!")
            return False, False, False
        return ret, frame, self.encode_im(frame)

    def encode_im(self, image):
        # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
        # '.jpg'表示将图片按照jpg格式编码。
        result, imgencode = cv2.imencode('.jpg', image, self.encode_param)

        # 建立矩阵
        data = numpy.array(imgencode)

        # 将numpy矩阵转换成字符形式，以便在网络中传输
        stringData = data.tostring()
        return stringData


def client_camera(ip, port, camera_name, signalLock, allsignal):

    if len(camera_name) < 3:
        camera_name = int(camera_name)

    print(f"ip: {ip},  port:{port},  camera_id:{camera_name}")

    cam_send = MyCameraSend(camera_name)
    socket_bind = SocketBind(ip, int(port))

    while True:
        start = time.time()  # 用于计算帧率信息
        ret, frame, stringData = cam_send.read()
        if not ret:
            print("not capture camera!!")
            break
        socket_bind.send(stringData)
        recvdata = socket_bind.receive()
        if port == 8386:
            # print(f" {start} {port} done recv{recvdata}")
            with signalLock:
                allsignal['s'] = copy.deepcopy(recvdata)
    socket_bind.close()



