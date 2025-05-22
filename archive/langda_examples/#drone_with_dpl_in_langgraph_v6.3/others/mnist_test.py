import torch
from deepproblog.evaluate import get_confusion_matrix
from deepproblog.examples.MNIST.data import MNIST_test, addition
from deepproblog.examples.MNIST.network import MNIST_Net
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.engines import ExactEngine
import config as cf
import os

method = "exact"
N = 1

# 数据集
test_set = addition(N, "test")

# 初始化网络
network = MNIST_Net()
net = Network(network, "mnist_net", batching=True)

# 初始化模型
model = Model(cf.CHANGED_RULE_PATH, [net])
model.set_engine(ExactEngine(model), cache=True)
model.add_tensor_source("test", MNIST_test)

# 正确加载模型权重 ✅
model.load_state(os.path.join(cf.CURRENT_PATH, "models/addition_exact_1.pth"))

# 测试
accuracy = get_confusion_matrix(model, test_set, verbose=2).accuracy()
print("Test accuracy:", accuracy)
