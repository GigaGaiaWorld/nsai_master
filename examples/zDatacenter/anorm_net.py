import torch

from deepproblog.dataset import DataLoader
from deepproblog.engines import ExactEngine
from deepproblog.evaluate import get_confusion_matrix
# 如果已有传感器数据集，请替换下面的导入
# from your_sensor_dataset import train_dataset, test_dataset

from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.train import train_model
from deepproblog.utils.standard_networks import MLP
from deepproblog.utils.stop_condition import Threshold, StopOnPlateau

from dataset import train_dataset, test_dataset
from networks import SensorNet

from problog.logic import _arithmetic_functions
# _arithmetic_functions[("tensor", 1)] = lambda x: x.item() if hasattr(x, "item") else float(x)
# _arithmetic_functions[("nn", 2)] = lambda x: x.item() if hasattr(x, "item") else float(x)


batch_size = 5
loader = DataLoader(train_dataset, batch_size)
lr = 1e-3

# 温度网络，对应 ds_ie1_multinets.pl 中的 nn(temp_net, ...)

# # 湿度网络，对应 ds_ie1_multinets.pl 中的 nn(humi_net, ...)
# humi_network = SensorNet(num_classes=2)
# humi_net = Network(humi_network, "humi_net", batching=True)
# humi_net.optimizer = torch.optim.Adam(humi_net.parameters(), lr=lr)

# 温度网络，对应 ds_ie1_multinets.pl 中的 nn(temp_net, ...)
temp_network = SensorNet(num_classes=2)
temp_net = Network(temp_network, "temp_net", batching=True)
temp_net.optimizer = torch.optim.Adam(temp_net.parameters(), lr=lr)

# CPU 负载网络，对应 ds_ie1_multinets.pl 中的 nn(cpul_net, ...)
cpul_network = SensorNet(num_classes=2)
cpul_net = Network(cpul_network, "cpul_net", batching=True)
cpul_net.optimizer = torch.optim.Adam(cpul_net.parameters(), lr=lr)
model = Model("new.pl", [temp_net,cpul_net])

# 使用 ds_ie1_multinets.pl 定义的逻辑规则和 nn 谓词
# model = Model("generated/example_for_netowork/ds_ie2_multinets.pl", [temp_net, cpul_net, humi_net])
model.add_tensor_source("train", train_dataset)
model.add_tensor_source("test", test_dataset)
model.set_engine(ExactEngine(model), cache=True)

train_obj = train_model(
    model,
    loader,
    StopOnPlateau("Accuracy", warm_up=10, patience=10)
    | Threshold("Accuracy", 1.0, duration=2),
    log_iter=100 // batch_size,
    test_iter=100 // batch_size,
    test=lambda x: [("Accuracy", get_confusion_matrix(x, test_dataset).accuracy())],
    infoloss=0.25,
)
