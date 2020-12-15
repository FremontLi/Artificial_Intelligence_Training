from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import cv2 as cv

# 线程介绍
# 继承线程类 
# 必须重写run方法  run：线程的功能（读取视频帧）
# start方法执行线程

class Video(QThread):

    #1 定义信号 传递的数据类型
    sign_show = pyqtSignal(int, int, int,  bytes)


    def __init__(self):
        super(Video,self).__init__()

        # 准备视频流
        # 1>摄像头
        self.dev = cv.VideoCapture(0,cv.CAP_DSHOW)

    # 2 重写run方法
    def run(self):

        # 循环 逐帧捕获
        while True:
            # 拿到每一帧图片数据          
            status, frame = self.dev.read()
            h,w,c = frame.shape

            #3 发送信号 传递数据 
            self.sign_show.emit(h,w,c,frame.tobytes())

            # 等待 0.1秒  100000微妙
            QThread.usleep(100000)