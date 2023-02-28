# https://blog.csdn.net/qq_39290394/article/details/84696100
import socket
import time
import cv2
import numpy as np
import pickle
import copy
import sys


class SocketServer:
    def __init__(self, ip='0.0.0.0', port=8002):
        # IP地址'0.0.0.0'为等待客户端连接
        self.address = (ip, port)
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # self.sock.setsockopt(socket.SOL_SOCKET, )

        # 将套接字绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址.
        self.sock.bind(self.address)

        # 开始监听TCP传入连接。参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。
        self.sock.listen(1)

        # 图片为空
        self.image = None

        self.olIndex = [1, 3, 5]
        self.bsIndex = [0, 2, 4, 6]
        self.sendMessage = ['1', '1', '1', '1', '1', '1', '1']
        self.last_sendMessage = np.copy(self.sendMessage)
        self.sendMessage = np.array(self.sendMessage)

    def accept(self):
        self.conn, self.addr = self.sock.accept()
        self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。addr是连接客户端的地址。
        # 没有连接则等待有连接
        print('connect from:' + str(self.addr))

    def recvall(self, sock, count):
        buf = b''  # buf是一个byte类型
        while count:
            # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def send(self, sock1, streamData):
        # 先发送要发送的数据的长度
        # ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
        sock1.send(str.encode(str(len(streamData)).ljust(16)))
        # 发送数据
        sock1.send(streamData)

    def receive(self):
        length = self.recvall(self.conn, 16)  # 获得图片文件的长度,16代表获取长度
        stringData = self.recvall(self.conn, int(length))  # 根据获得的文件长度，获取图片文件
        data = np.frombuffer(stringData, np.uint8)  # 将获取到的字符流数据转换成1维数组
        self.image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像

    def deal_send(self, decimg):
        image = decimg
        if image is not None:
            sendstring = "chuli"
            """ 处理加处理结果
            """
            send_data = pickle.dumps(sendstring)
            self.send(self.conn, send_data)

        self.image = None

    def sendResMessage(self, msg):
        self.sendMessage=list(msg)
        # print(f"self.sendMessage:{self.sendMessage}")
        # if msg is not None:
        #     comOlMsg = msg['message']
        #     olImg = msg['img']
        #     olOriImg = msg['oriImg']
        #     comOlMsg = list(comOlMsg)
        #     comOlMsg = np.array(comOlMsg)
        #     sickerState = comOlMsg[self.olIndex]
        #     self.sendMessage[self.olIndex] = comOlMsg[self.olIndex]
        #     self.sendMessage[self.bsIndex] = comOlMsg[self.bsIndex]

        flags_dige = True
        for _ in range(7):
            if self.last_sendMessage[_] != '0':
                flags_dige = False
                break
        status_index = [2, 4, 6]
        if self.sendMessage[0] == '0' and flags_dige:
            for _ in range(7):
                self.sendMessage[_] = self.last_sendMessage[_]
        elif self.sendMessage[0] == '0':
            nums_hs = 0
            for _ in status_index:
                # if last_sendMessage[_] == '0' and last_sendMessage[_ - 1] == '0':
                #     sendMessage[_] = '0'
                #     sendMessage[_ - 1] = '0'
                if self.last_sendMessage[_] != self.sendMessage[_]:
                    nums_hs += 1
            if nums_hs > 1:
                for _ in status_index:
                    self.sendMessage[_] = self.last_sendMessage[_]
            # if nums_hs > 0:
            #     print(nums_hs, end='   ')
            #     print(type_str)

        for _ in range(7):
            self.last_sendMessage[_] = self.sendMessage[_]

        # send to UI
        if self.sendMessage[0] == '1':
            for i in range(len(self.sendMessage)):
                self.sendMessage[i] = '1'

        type_str = "".join(self.sendMessage)

        send_data = pickle.dumps(type_str)
        self.send(self.conn, send_data)

    def close(self):
        self.sock.close()


def tcpServer(ip, port, camFrameDict, syncLock , shareMsg):
    # port = 8002
    print(f"ip: {ip},  port{int(port)}")
    server = SocketServer(port=int(port))
    while True:
        try:
            start = time.time()  # 用于计算帧率信息
            decimg = server.receive()
            end = time.time()
            seconds = end - start
            fps = 1 / seconds
            # print(f"receive:{seconds*1000}")
            with syncLock:
                camFrameDict['f'] = np.copy(decimg)
            olMessage = None
            # if not resQueue.empty():
            #     olMessage = resQueue.get_nowait()
            #     if port == 8382:
            #         print(f"olMessage['message']:{olMessage['message']}")
            # print(f"tcp shareMsg:{shareMsg.value}")

            start = time.time()
            server.sendResMessage(copy.deepcopy(shareMsg.value))
            end = time.time()
            seconds = end - start
            # print(f"receive:{seconds * 1000}")

            # print("done send")
            # 将帧率信息回传，主要目的是测试可以双向通信
            # end = time.time()
            # seconds = end - start
            # fps = 1 / seconds
            # print(fps)
            cv2.imshow('SERVER', decimg)  # 显示图像
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
        except:
            server.accept()
    server.close()
    cv2.destroyAllWindows()
