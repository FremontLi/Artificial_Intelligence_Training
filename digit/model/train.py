# 层
# 线性层（全连接层） 堆叠多个线性层 不能帮助神经网络学习新的东西 
# 非线性激活函数
# 卷积层

# 基于解决的问题确定最后一层
# 1 回归问题 输出线性层
# 2 二分类 使用sigmoid函数
# 3 多分类 输出线性层 然后使用类（softmax）函数输出给定数量的样例的概率  和为1
# 损失函数
# 回归问题 均方误差函数
# 分类问题 交叉熵损失函数

# 数据集
# 目录结构必须遵守固定规则
# 第三方框架的处理[]
import os
import sys

import loader as loader
import torch
import torch.utils.data

from lenet import LeNet5


class TrainLeNet:
    # 构造函数  数据集路径ds_dir   轮数  学习率
    def __init__(self, epoch=1000, lr=0.0001):
        super(TrainLeNet, self).__init__()

        print("训练准备.......")  # 开始
        # 二进制模型文件
        self.model_file = "lenet.pth"
        # self.CUDA true false
        self.CUDA = torch.cuda.is_available()

        self.train_loader, self.test_loader = loader.load_data()

        self.net=LeNet5()
        params = self.net.parameters()
        if self.CUDA:
            self.net.cuda()
        if os.path.exists(self.model_file):
            print("加载本地模型")
            # 加载本地模型
            state = torch.load(self.model_file)
            self.net.load_state_dict(state)

        # 3、参数
        self.epoch = epoch
        self.lr = lr
        # 损失函数
        self.loss_function = torch.nn.CrossEntropyLoss()

        # 优化器 学习率
        self.optimizer = torch.optim.Adam(self.net.parameters(),self.lr)

        if self.CUDA:
            self.loss_function = self.loss_function.cuda()


    def execute(self):
        for e in range(self.epoch):
            # 1轮 整个训练数据集 学习一次
            print(F"第{e + 1:02d}轮")
            for data, target in self.train_loader:
                # 1 批
                # print(data.shape)
                # print(target.shape)
                # 批处理
                # 批梯度下降 权重更新

                # 导数清零
                self.optimizer.zero_grad()
                # 使用模型预测
                out = self.net(data)
                # 训练时dim=1,使用时dim=0
                out = torch.nn.functional.log_softmax(out, dim=1)
                # out target  计算损失
                loss = self.loss_function(out, target)
                # 求导
                loss.backward()
                # 更新权重
                self.optimizer.step()
            # 每轮 验证准确率  使用测试数据集
            # 使用数据集验证
            correct_rate = self.validate()
            print(F"轮数：{e + 1:03d}")
            print(F"正确率：{correct_rate:5.4f}%")
            print(F"损失值：{loss:8.6f}")
        # 保存模型 整个网络结构和参数
        # torch.save(self.net, "lenet.pth")
            torch.save(self.net.state_dict(),"lenet.pth")  #整个参数 二进制保存有自己特殊的规则
        # 可视化在线工具 查看模型 结构  https://netron.app/

    @torch.no_grad()
    def validate(self):
        num_samples = 0.0
        num_correct = 0.0
        self.net.eval()
        for samples, labels in self.test_loader:
            if self.CUDA:
                samples = samples.cuda()
                labels = labels.cuda()
            num_samples += len(samples)
            # 计算输出
            out = self.net(samples)
            # 激活 0--1
            out = torch.nn.functional.softmax(out, dim=1)
            # 概率最大的类别下标和概率值
            y = torch.argmax(out, dim=1)
            num_correct += (y == labels).float().sum()
        return num_correct * 100.0 / num_samples


if (len(sys.argv)) >=3:
    trainer = TrainLeNet(int(sys.argv[1]),float(sys.argv[2]))
else:
    trainer = TrainLeNet()

trainer.execute()