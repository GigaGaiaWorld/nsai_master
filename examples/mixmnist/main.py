from json import dumps

import torch
from typing import Dict, Tuple, Iterable

from deepproblog.dataset import DataLoader
from deepproblog.engines import ApproximateEngine, ExactEngine
from deepproblog.evaluate import get_confusion_matrix
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.train import train_model

from langda import langda_solve
from .mixmnist import MIXMNIST
from .operation import MNISTOperator
from .network import MNIST_Net

# =============== define some (prompt, function) pairs
def my_sum(input:Iterable[int | bool]):
    return sum(input)

def my_cone_volume(input:Iterable[int | bool]):
    radius = input[0]
    height = input[1]
    return round((1/3) * 3.14 * radius**2 * height)
def my_swap(input:Iterable[int | bool]):
    """ [4,8] => 84"""
    return input[1] * 10 + input[0]

FUNCMAP = {
    "Arabic":("This is for arabic numbers. Please calculate the sum of X and Y elements. Example: Input [3, True, False] → 3+1+0=4",my_sum),
    "Telugu":("This is for telugu numbers. Please calculate the volume of the cone. X is the base radius, Y is the height, π is approximated to 3.14",my_cone_volume),
    "Urdu":("This is for urdu numbers. Please swap the positions of X and Y and combine them into a new number. Example: input [4,8] → 8*10 + 4 = 84",my_swap),
}

language = "Arabic"


def operation(n: int, dataset: str, language:str, func:callable, seed=None):
    """Returns a dataset for binary addition"""
    return MNISTOperator(
        dataset_name=dataset,
        function_name="operation",
        operator=func,
        size=n,
        arity=2,
        seed=seed,
        prefix=language
    )

method = "exact"
N = 1

name = "operation_{}_{}".format(method, N)

train_set = operation(N, "train", language, my_swap, seed=42)
test_set = operation(N, "test", language, my_swap, seed=42)
 
MIXMNIST_train = MIXMNIST(prefix=language, subset="train")
MIXMNIST_test = MIXMNIST(prefix=language, subset="test")

network1 = MNIST_Net()
network2 = MNIST_Net()
network3 = MNIST_Net()

# pretrain = 0
# if pretrain is not None and pretrain > 0:
#     network.load_state_dict(torch.load("models/pretrained/all_{}.pth".format(pretrain)))

net1 = Network(network1, "arabic_net", batching=True)
net1.optimizer = torch.optim.Adam(network1.parameters(), lr=1e-3)
net2 = Network(network2, "telugu_net", batching=True)
net2.optimizer = torch.optim.Adam(network2.parameters(), lr=1e-3)
net3 = Network(network3, "urdu_net", batching=True)
net3.optimizer = torch.optim.Adam(network3.parameters(), lr=1e-3)


with open("operation.pl", "r") as f:
    rule_string = f.read()

result_string = langda_solve("single_dc", rule_string,
                        additional_input={
                            "langda_ext": {"PROMPT":FUNCMAP[language][0]}})

model = Model(result_string, [net1,net2,net3])
if method == "exact":
    model.set_engine(ExactEngine(model), cache=True)

model.add_tensor_source("train", MIXMNIST_train)
model.add_tensor_source("test", MIXMNIST_test)

loader = DataLoader(train_set, 2, False)
train = train_model(model, loader, 2, log_iter=100, profile=0)
model.save_state("snapshot/" + name + ".pth")
train.logger.comment(dumps(model.get_hyperparameters()))
train.logger.comment(
    "Accuracy {}".format(get_confusion_matrix(model, test_set, verbose=1).accuracy())
)
train.logger.write_to_file("log/" + name)
