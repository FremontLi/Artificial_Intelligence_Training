import struct
import numpy as np
# 读取图片
import torch


def load_image_fromfile(filename):
    with open(filename, 'br') as fd:
        # 读取图像的信息
        header_buf = fd.read(16)   # 16字节，4个int整数
        # 按照字节解析头信息（具体参考python SL的struct帮助）  解包
        magic_, nums_, width_, height_ = struct.unpack('>iiii', header_buf)  # 解析成四个整数：>表示大端字节序，i表示4字节整数
        # 保存成ndarray对象
        imgs_ = np.fromfile(fd, dtype=np.uint8)
        imgs_ = imgs_.reshape(nums_, height_, width_)
    return imgs_


# 读取标签
def load_label_fromfile(filename):
    with open(filename, 'br') as fd:
        header_buf = fd.read(8) 
        magic, nums = struct.unpack('>ii' ,header_buf) 
        labels_ = np.fromfile(fd, np.uint8) 
    return labels_


def load_data():
    # 读取训练数据集
    # 图片
    train_x = load_image_fromfile('data/train-images.idx3-ubyte')
    train_y = load_label_fromfile('data/train-labels.idx1-ubyte')
    # print(train_x.shape)# N数量 H W

    # 读取测试数据集
    # 图片
    test_x = load_image_fromfile('data/t10k-images.idx3-ubyte')
    test_y = load_label_fromfile('data/t10k-labels.idx1-ubyte')

    x = torch.Tensor(train_x).view(train_x.shape[0], 1, train_x.shape[1], train_x.shape[2])
    y = torch.LongTensor(train_y)

    t_x = torch.Tensor(test_x).view(test_x.shape[0], 1, test_x.shape[1], test_x.shape[2])
    t_y = torch.LongTensor(test_y)

    # 使用torch封装数据
    train_dataset = torch.utils.data.TensorDataset(x, y)
    test_dataset = torch.utils.data.TensorDataset(t_x, t_y)

    # 数据随机加载 按批切分   （数据加载器）
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, shuffle=True, batch_size=2000)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, shuffle=True, batch_size=10000)

    return train_loader, test_loader