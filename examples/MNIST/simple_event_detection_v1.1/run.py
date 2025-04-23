import os
import re
import sys

from mnist import MNIST_Net, test_MNIST, neural_predicate

sys.path.append('/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/')

from src.deepprobcep.test_utils import get_confusion_matrix, calculate_f1
from sounds_utils import SoundVGGish, neural_predicate_vggish
from prob_ec_testing import test
from src.deepprobcep.model import Model, Var
from src.deepprobcep.train import train_model
from src.deepprobcep.data_loader import load
from src.deepprobcep.optimizer import Optimizer
from src.deepprobcep.network import Network
import torch

def add_files_to(problog_files, problog_string):
    for problog_file in problog_files:
        with open(problog_file) as f:
            problog_string += f.read()
            problog_string += '\n\n'

    return problog_string

def my_test(model_to_test, test_queries, test_functions=None):
    res = test(model_to_test, test_queries, test_functions=test_functions)

    # res += test_MNIST(model_to_test)

    return res


def run(training_data, test_data, problog_files, problog_train_files=(), problog_test_files=()):
    queries = load(training_data)
    test_queries = load(test_data)

    problog_string = add_files_to(problog_files, '')

    problog_train_string = add_files_to(problog_train_files, problog_string)
    problog_test_string = add_files_to(problog_test_files, problog_string)

    network1 = MNIST_Net(N=3)
    net1 = Network(network1, 'mnist_net1', neural_predicate)
    net1.optimizer = torch.optim.Adam(network1.parameters(), lr=0.001)

    network2 = MNIST_Net(N=2)
    net2 = Network(network2, 'mnist_net2', neural_predicate)
    net2.optimizer = torch.optim.Adam(network2.parameters(), lr=0.001)

    model_to_train = Model(problog_train_string, [net1,net2], caching=False)
    optimizer = Optimizer(model_to_train, 2)

    model_to_test = Model(problog_test_string, [net1,net2], caching=False)

    train_model(
        model_to_train,
        queries, 
        5, # epoches
        optimizer,
        test_iter=len(queries),
        test=lambda _: my_test(
            model_to_test,
            test_queries,
            test_functions={
                'mnist_net1': lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test'),
                'mnist_net2': lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test')
            },
        ),
        log_iter=1000,
        snapshot_iter=len(queries)
    )


if __name__ == '__main__':
    model_path = "model"
    prob_ec_cached = os.path.join(model_path,"prob_ec_cached.pl")
    event_defs = os.path.join(model_path,"event_occ_defs.pl")
    alltimestamps = os.path.join(model_path,"alltimestamps.txt")

    run(
        'init_train_data.txt', # original: holds_train_data.txt
        'init_test_data.txt', # init_test_data.txt
        [event_defs, alltimestamps],
        problog_train_files=['in_train_data.txt'],  # Put in a list
        problog_test_files=['in_test_data.txt']     # Put in a list
    )
