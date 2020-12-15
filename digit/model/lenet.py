import torch
class LeNet5(torch.nn.Module):
    # 重写
    # __init__  定义层
    # forward   计算
    def __init__(self):
        super(LeNet5,self).__init__()
        # 层  torch.nn.层
        # N 60000
        # C 1
        # H 28
        # W 28

        # 卷积1 1 28*28  ---> 6 28*28     操作池化 6 14*14
        # 卷积2 6 14*14  ---> 16 10*10     操作池化 16 5*5
        # 卷积3 16 5*5  ---> 120 1*1   
        # 全连接 120 --> 84
        # 全连接 84 --> 10
        self.layer1 = torch.nn.Conv2d(in_channels=1,out_channels=6,kernel_size=(5,5),padding=2)
        self.layer2 = torch.nn.Conv2d(in_channels=6,out_channels=16,kernel_size=(5,5),padding=0)
        self.layer3 = torch.nn.Conv2d(in_channels=16,out_channels=120,kernel_size=(5,5),padding=0)
        self.layer4 = torch.nn.Linear(120,84)
        self.layer5 = torch.nn.Linear(84,10)

    def forward(self,input):
        # 使用定义好的层计算
        # 第1层计算
        t = self.layer1(input)
        # 激活函数 池化
        t = torch.nn.functional.relu(t)
        t = torch.nn.functional.max_pool2d(t,kernel_size=(2,2))
        # __init__ self.layer1_1 = torch.nn.MaxPool2d(kernel_size=(2,2))
        # t = self.layer1_1(t)

        # 第2层计算
        t = self.layer2(t)
        # 激活函数 池化
        t = torch.nn.functional.relu(t)
        t = torch.nn.functional.max_pool2d(t,kernel_size=(2,2))

        # 第3层计算
        t = self.layer3(t)
        # 激活函数
        t = torch.nn.functional.relu(t)
        # 1维度 N*120*1*1 降维 N*120   
        t = t.squeeze()

        # 第4层计算
        t = self.layer4(t)
        # 激活函数
        t = torch.nn.functional.relu(t)

        # 第5层计算
        t = self.layer5(t)
        # t = torch.nn.functional.log_softmax(t,dim=1)
        return t 




