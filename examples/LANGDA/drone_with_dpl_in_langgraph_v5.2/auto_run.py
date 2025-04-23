import os
import sys

from typing import List, Tuple, Dict, Union
from mnist import MNIST_Net, MNIST_Classifier, test_MNIST, neural_predicate

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from prob_ec_testing import test
from src.deepprobcep.model import Model
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


def construct_network_list(net_str_list:List[Tuple[str,int]]) -> List[Network]:
    net_list = []
    net_info_list = []
    for (net_str,dim_out) in net_str_list:
        if "mnist" in net_str:
            network = MNIST_Net(N=dim_out)
            net = Network(network, net_str, neural_predicate)
            net.optimizer = torch.optim.Adam(network.parameters(), lr=0.001)
            net_list.append(net)
        # this is just a demo......
        # we could write this into a cleaner version later
        if "clasifier" in net_str:
            network = MNIST_Classifier(N=dim_out)
            net = Network(network, net_str, neural_predicate)
            net.optimizer = torch.optim.Adam(network.parameters(), lr=0.001)
            net_list.append(net)

    return net_list


def my_test(net_str_list:List[Tuple[str,int]], 
            test_data:str, 
            problog_files:List[str], problog_test_files:List[str], load_model=()) -> list:
    
    test_queries = load(test_data)

    problog_string = add_files_to(problog_files, '\n')
    problog_test_string = add_files_to(problog_test_files, problog_string)

    net_list = construct_network_list(net_str_list)
    test_functions={
        # dataset='test': use for "event" to find corresponding image from MNIST dataset
        net.name: lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test') for net in net_list
    }

    print("testing...")
    model_to_test = Model(problog_test_string, net_list, caching=False)
    model_to_test.load_state(load_model)

    result = test(model_to_test, 
                    test_queries, 
                    test_functions,
                    )
        
    return result


def my_train(net_str_list:List[Tuple[str,int]], 
            training_data:str, test_data:str, 
            problog_files:List[str], problog_train_files:List[str], problog_test_files:List[str]) -> dict:
    
    train_queries = load(training_data)
    test_queries = load(test_data)

    problog_string = add_files_to(problog_files, '\n')
    problog_train_string = add_files_to(problog_train_files, problog_string)
    problog_test_string = add_files_to(problog_test_files, problog_string)

    net_list = construct_network_list(net_str_list)
    test_functions={
        # dataset='test': use for "event" to find corresponding image from MNIST dataset
        net.name: lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test') for net in net_list
    }

    print("training...")
    model_to_train = Model(problog_train_string, net_list, caching=False)
    optimizer = Optimizer(model_to_train, 2)  # In Optimizer class, step function, clean gradient each 2 steps
    # should be noticed is that here net1 and net2 are already instances, 
    # so since model_to_test is built with them, it is also the instance of training model.
    model_to_test = Model(problog_test_string, net_list, caching=False)

    result:dict = train_model(
        model_to_train,
        train_queries,
        optimizer,

        test_function=lambda _: test(
            model_to_test,
            test_queries,
            test_functions,
        ),

        nr_epochs=5,                    # training epoches
        log_iter=10,                   # output "Average Loss" each X Iterations
        snapshot_name="models/model"    # save model name
    )

    return result

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(dir_path, "data/origin")
    rules_path = os.path.join(dir_path, "rules/basic")
    model_path = os.path.join(dir_path, "models")

    result = my_train(
        [("mnist_net1",2), ("mnist_net2",2)],
        os.path.join(data_path,'detect_train_data.txt'),                     # training_data: detect_train_data.txt detectEvent
        os.path.join(data_path,'detect_test_data.txt'),                      # test_data: detect_test_data.txt  detectEvent
        [
            # os.path.join(model_path,"event_occ_defs.pl"),                  # problog_files: ruleset,
            os.path.join(rules_path,"DeE_ResDeE.pl"),          # problog_files: ruleset,
        ],
        [os.path.join(data_path,'in_train_data.txt')],                      # problog_train_files: happensAt (put a list here)
        [os.path.join(data_path,'in_test_data.txt')],                       # problog_test_files: happensAt (put a list here)
        # os.path.join(model_path,'model_iter_basic_detect.mdl'),             # load_model: 
    )
    print(f"=====================final result=====================\n{result}")