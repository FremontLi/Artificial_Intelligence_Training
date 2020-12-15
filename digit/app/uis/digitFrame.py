import numpy as np
from PyQt5.QtWidgets import QDialog, QWidget, QFileDialog

from app.core.recognizer import DigitRecognizer
from app.core.video import Video
from app.uis.digitui import Ui_Dialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.Qt import Qt
import cv2


class DigitFrame(QDialog):
    def __init__(self, *args):
        super(DigitFrame, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # 线程
        self.th = Video()

        # 5 信号连接到槽函数
        self.th.sign_show.connect(self.show_video)

        # 6 启动线程
        self.th.start()

    def show_video(self, h, w, c, data):
        # 存取相关data用于截图
        self.videoData = {'data': data, 'h': h, 'w': w, 'c': c}
        imgae = QImage(data, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(imgae)
        # 自动缩放
        width = self.ui.lblImg.width()
        height = self.ui.lblImg.height()
        scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.lblImg.setPixmap(scale_pix)

    # 截图
    def cutImage(self):
        data = self.videoData['data']
        h = self.videoData['h']
        w = self.videoData['w']
        c = self.videoData['c']
        # 读取图片，将字节流格式转成cv格式
        cv_image = np.frombuffer(data, dtype=np.uint8).reshape(h, w, c)
        self.cv_image = cv_image
        self.show_image()

    # 获取文件路径
    def loadImage(self):
        self.fileName = QFileDialog.getOpenFileName(self)[0]
        self.cv_image = cv2.imread(self.fileName)
        self.show_image()

    def recognize(self):
        print("开始识别")
        recognizer = DigitRecognizer()
        cls, p = recognizer.recognize(self.cv_image)
        self.ui.lblResult.setText(str(cls.numpy()))
        print(cls)
        print(p)

    # 展示图片
    def show_image(self):
        # 读取图片
        img_data = self.cv_image
        # cv图片转换成QT能显示的数据格式
        h, w, c = img_data.shape
        data = img_data.tobytes()
        imgae = QImage(data, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(imgae)
        width = self.ui.lblImg_cut.width()
        height = self.ui.lblImg_cut.height()
        scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.lblImg_cut.setPixmap(scale_pix)
        self.recognize()
