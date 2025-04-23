import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

class MNIST_Net(nn.Module):
    """
    input:
    output:
    """
    def __init__(self, N=10):
        super(MNIST_Net, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1,  6, 5), # [1, 1, 28, 28]
            nn.MaxPool2d(2, 2), # 6 24 24 -> 6 12 12
            nn.ReLU(True),
            nn.Conv2d(6, 16, 5), # 6 12 12 -> 16 8 8
            nn.MaxPool2d(2, 2), # 16 8 8 -> 16 4 4
            nn.ReLU(True),
        )
        self.classifier =  nn.Sequential(
            nn.Linear(16 * 4 * 4, 240),
            nn.ReLU(),
            nn.Linear(240, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, N),
            nn.Softmax(1),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = x.view(-1, 16 * 4 * 4)
        x = self.classifier(x)
        return x

class MNIST_Classifier(nn.Module):
    def __init__(self, N=10, with_softmax=True):
        super(MNIST_Classifier, self).__init__()
        self.with_softmax = with_softmax
        if with_softmax:
            self.softmax = nn.Softmax(1)
        self.classifier = nn.Sequential(

            nn.Linear(28 * 28, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, N),
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        if self.with_softmax:
            x = self.softmax(x)
        return x.squeeze(0)


def test_MNIST(model,max_digit=10,name='mnist_net'):
    confusion = np.zeros((max_digit,max_digit),dtype=np.uint32) # First index actual, second index predicted
    N = 0
    for d,l in mnist_test_data:
        if l < max_digit:
            N += 1
            d = Variable(d.unsqueeze(0))
            outputs = model.networks[name].net.forward(d)
            _, out = torch.max(outputs.data, 1)
            c = int(out.squeeze())
            confusion[l,c] += 1
    print(confusion)
    F1 = 0
    for nr in range(max_digit):
        TP = confusion[nr,nr]
        FP = sum(confusion[:,nr])-TP
        FN = sum(confusion[nr,:])-TP
        F1 += 2*TP/(2*TP+FP+FN)*(FN+TP)/N
    print('F1: ',F1)
    return [('F1',F1)]


def neural_predicate(network, i, dataset='train'):
    i = int(i)
    dataset = str(dataset)
    if dataset == 'train':
        d, l = mnist_train_data[i]
    elif dataset == 'test':
        d, l = mnist_test_data[i]
    d = Variable(d.unsqueeze(0))
    output = network.net(d)
    return output.squeeze(0)

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5, ))])
mnist_train_data = torchvision.datasets.MNIST(root=dir_path+'/../../../data/MNIST', train=True, download=True,transform=transform)
mnist_test_data = torchvision.datasets.MNIST(root=dir_path+'/../../../data/MNIST', train=False, download=True,transform=transform)
