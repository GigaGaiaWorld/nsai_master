import torch
import os
import sys
# sys.path.append('../../../')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from problog.logic import Var
from src.deepprobcep.test_utils import get_confusion_matrix, calculate_f1, calculate_accuracy

CONFUSION_INDEX = {
    'event': {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
    },
    'detectEvent': {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
    },
    'result': {
        'win=0': 0,
        'win=1': 1,
   },
}
#=================#=================# event #=================#================='
def get_target_event(query):
    target = query.args[1]

    return str(target)

def query_transformation_event(query):
    args0, _ = query.args
    # print("query_transformation_digit:", query(args0, Var('X')))
    return query(args0, Var('X'))

def get_result_event(output):
    k, v = list(output.items())[0]
    result = str(k.args[1])
    prob = v[0]
    # print("get_result_digit:", result)
    return result

#=================#=================# result #=================#================='
def get_target_result(query):
    target = query.args[0]
    # print("get_target_initiated_at:", str(target))
    return str(target)

def query_transformation_result(query):
    args0, args1 = query.args
    # print("query_transformation_initiated_at:",query(args0(Var('sequence'), Var('Y')), args1))
    return query(args0(Var('win'), Var('Y')), args1)

def get_result_result(output):
    k, v = list(output.items())[0]
    result = str(k.args[0])
    prob = v[0]
    # print("get_result_initiated_at:", result)

    return result

#=================#=================# detect_event #=================#================='
def get_target_detect_event(query):
    target = query.args[0]
    # print("get_target_holds_at:", str(target))

    return str(target)

def query_transformation_detect_event(query):
    args0, args1 = query.args

    return query(Var('X'), args1)

def get_result_detect_event(output):
    k, v = list(output.items())[0]
    result = str(k.args[0])
    prob = v[0]

    return result


TEST_METHODS = {
    'event': (get_target_event, query_transformation_event, get_result_event),

    'detectEvent': (get_target_detect_event, query_transformation_detect_event, get_result_detect_event),

    'result': (get_target_result, query_transformation_result, get_result_result),
    'detectE': (get_target_result, query_transformation_result, get_result_result),

}


def test(model, test_queries, test_functions=None, confusion_index=None, test_methods=None):
    # Substitute the functions to the test ones
    if confusion_index is None:
        confusion_index = CONFUSION_INDEX
    if test_methods is None:
        test_methods = TEST_METHODS


    original_functions = {
        net_name: model.networks[net_name].function
        for net_name in model.networks
    }
    if test_functions:
        for net_name, new_func in test_functions.items():
            try:
                model.networks[net_name].function = new_func
            except Exception as e:
                print("test function:",e)
    with torch.no_grad():
        confusion_dict = get_confusion_matrix(
            model, confusion_index, test_queries, test_methods
        )
    res_list = []

    #==========================================================================#
    #======== write to confusion_index&test_queries&test_methods.txt ==========#
    with open ("test_utils.txt", 'w') as complex_f:

        # complex_f.write(f"confusion_index:\n{confusion_index}\n")
        # complex_f.write(f"test_queries:\n{test_queries}\n")
        # complex_f.write(f"test_methods:\n{test_methods}\n")
        # complex_f.write(f"confusion_dict:\n{confusion_dict}\n")
    
        for k, confusion in confusion_dict.items():
            f1 = calculate_f1(confusion)

            accuracy = calculate_accuracy(confusion)

            print(k)
            print(confusion)

            f1_text = 'F1 {}: {}'.format(k, f1)
            print(f1_text)

            res_list.append(
                ('F1 {}'.format(k), f1)
            )

            acc_text = 'Accuracy {}: {}'.format(k, accuracy)
            print(acc_text)

            res_list.append(
                ('Accuracy {}'.format(k), accuracy)
            )
            complex_f.write(f"{f1_text}")
            complex_f.write(f"{acc_text}")
    # Restore the original function
    for net_name, ori_func in original_functions.items():
        model.networks[net_name].function = ori_func

    return res_list
