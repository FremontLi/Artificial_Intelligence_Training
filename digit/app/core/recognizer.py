import torch
from torchvision.models import resnet18
from torchvision.transforms import Resize, Compose, ToTensor, Normalize, RandomHorizontalFlip, RandomVerticalFlip, RandomResizedCrop
import cv2 as cv
from PIL import Image

from torchvision.datasets import ImageFolder

# 设置管道 类别和类别下标
from model.lenet import LeNet5


class DigitRecognizer:
    # 参数：模型文件的路径
    def __init__(self, model_file="model/lenet.pth"):
        super(DigitRecognizer, self).__init__()

        #1 设置模型文件

        # self.model_file = os.path.join(,model_file)
        self.model_file =  model_file
        # 判断cuda
        self.CUDA = torch.cuda.is_available()

        #2.模型定义
        self.net = LeNet5()
        params = self.net.parameters()

        if self.CUDA:
            self.net.cuda()

        #3.加载模型
        state = torch.load(self.model_file)
        self.net.load_state_dict(state)
        print("模型加载完毕！")
        self.net.eval()

    @torch.no_grad()
    # 参数：要识别的图片的路径
    def recognize(self,img):
        with torch.no_grad():
            # 返回固定格式的图片数据
            img = self.trans_data(img)
            if self.CUDA:
                img = img.cuda()
            # 预测
            y = self.net(img)

            # 激活  生成目标个数 概率
            p_y = torch.nn.functional.softmax(y, dim=0)
            # 概率最大的元素 概率值p和类别下标cls_idx
            p, cls_idx = torch.max(p_y, dim=0)

            return cls_idx, p

    # 传入cv图片
    def trans_data(self,img):
        # 转成灰度图片
        img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        img = cv.resize(img, (28, 28))
        img = torch.Tensor(img).view(1, 1, img.shape[0], img.shape[1])
        return img


