import os
import re
import sys

from mnist import MNIST_Net, MNIST_Classifier, test_MNIST, neural_predicate

sys.path.append('../../../')

from src.deepprobcep.test_utils import get_confusion_matrix, calculate_f1
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

def my_train(training_data, test_data, problog_files, problog_train_files=(), problog_test_files=(), 
        load_model=(), train_new_model=False, train_epochs=5):
    if train_new_model: train_queries = load(training_data)
    test_queries = load(test_data)

    problog_string = add_files_to(problog_files, '\n')
    if train_new_model: problog_train_string = add_files_to(problog_train_files, problog_string)
    problog_test_string = add_files_to(problog_test_files, problog_string)

    network1 = MNIST_Net(N=2)
    net1 = Network(network1, 'mnist_net1', neural_predicate)
    net1.optimizer = torch.optim.Adam(network1.parameters(), lr=0.001)

    network2 = MNIST_Net(N=2)
    net2 = Network(network2, 'mnist_net2', neural_predicate)
    net2.optimizer = torch.optim.Adam(network2.parameters(), lr=0.001)

    test_functions={
        # dataset='test': use for "event" to find corresponding image from MNIST dataset
        net1.name: lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test'),
        net2.name: lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test'),
    }    
    if train_new_model:
        print("training...")
        model_to_train = Model(problog_train_string, [net1,net2], caching=False)
        optimizer = Optimizer(model_to_train, 2)        
        model_to_test = Model(problog_test_string, [net1,net2], caching=False)
        train_model(
            model_to_train,
            train_queries,
            train_epochs, # epoches
            optimizer,

            test_iter=len(train_queries),
            test=lambda _: my_test(
                model_to_test,
                test_queries,
                test_functions,
            ),

            log_iter=1000,
            snapshot_iter=len(train_queries),
            snapshot_name="models/model"    # save model name
        )

    if not train_new_model:
        print("testing...")
        model_to_test = Model(problog_test_string, [net1,net2], caching=False)
        model_to_test.load_state(load_model)

        result = my_test(model_to_test, 
                    test_queries, 
                    test_functions,
                 )
        print("rule set:", problog_files)


if __name__ == '__main__':
    data_path = "data/origin"
    rules_path = "rules/basic"
    model_path = "models"
    my_train( 
        os.path.join(data_path,'result_train_data.txt'),                     # training_data: detect_train_data.txt detectEvent
        os.path.join(data_path,'result_test_data.txt'),                      # test_data: detect_test_data.txt  detectEvent
        [
            # os.path.join(model_path,"event_occ_defs.pl"),                  # problog_files: ruleset,
            os.path.join(rules_path,"DeE_ResDeE_rmNet.pl"),          # problog_files: ruleset,
        ],
        [os.path.join(data_path,'in_train_data.txt')],                      # problog_train_files: happensAt (put a list here)
        [os.path.join(data_path,'in_test_data.txt')],                       # problog_test_files: happensAt (put a list here)
        # os.path.join(model_path,'model_iter_basic_detect.mdl'),             # load_model: 
        train_new_model=True,              # train_new_model? or just test with existing model?
    )
