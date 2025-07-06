from json import dumps
import sys
from pathlib import Path

import torch
from typing import Dict, Tuple, Iterable, Literal

from deepproblog.dataset import DataLoader
from deepproblog.engines import ApproximateEngine, ExactEngine
from deepproblog.evaluate import get_confusion_matrix
from deepproblog.examples.MNIST.network import MNIST_Net
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.train import train_model

from langda import langda_solve
from mixmnist import MIXMNIST
from operation import MNISTOperator

current_dir = "examples/mixmnist"

query_ext = """digit(img_1,1).
arabic_digit(img_5,5).
arabic_digit(img_9,9).
arabic_digit(img_1,1).
telugu_digit(img_5,5).
telugu_digit(img_9,9).
telugu_digit(img_1,1).
kannada_digit(img_5,5).
kannada_digit(img_9,9).
kannada_digit(img_1,1).
urdu_digit(img_5,5).
urdu_digit(img_9,9).
urdu_digit(img_1,1).
query(anomaly_detection([img_9, img_1], [img_1, img_5], 1)).
query(anomaly_detection([img_5, img_1], [img_5, img_1], 1)).
query(anomaly_detection([img_9, img_5], [img_5, img_9], 1))."""

problog_string = """
% Neural network definitions for different languages
nn(arabic_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: arabic_digit(X,Y).
nn(telugu_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: telugu_digit(X,Y).
nn(kannada_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: kannada_digit(X,Y).
nn(urdu_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: urdu_digit(X,Y).

% Convert digit list to number
number([],Result,Result).
number([H|T],Acc,Result) :- 
    langda(LLM:"replace the 'digit(H,Nr)' here, with the appropriate language-specific digit predicate"), 
    Acc2 is Nr+10*Acc, number(T,Acc2,Result).
number(X,Y) :- number(X,0,Y).

% Anomaly detection logic - Result is 1 if anomaly detected, 0 otherwise
anomaly_detection(Digit1, Digit2, 1) :- 
    langda(LLM:"

Based on the geographic coordinate of user, determine which anomaly detection logic to use, 
1. If the user is in Saudi Arabia, check machine overheating anomaly:
   - If Temperature ≥ 60°C AND Flow rate ≤ 20 L/min, there's anomaly
   - number(Digit1, Temp), number(Digit2, Flow)

2. If the user is in Iraq, check storage tank Level anomaly:
   - If LiquidLevel ≥ 75% OR Pressure ≥ 15 bar, there's anomaly
   - number(Digit1, LiquidLevel), number(Digit2, Pressure)

3. If the user is in India, check power overload anomaly:
   - If sum of branch currents > 120A, there's anomaly
   - number(Digit1, Current1), number(Digit2, Current2)

4. If the user is in Urdu regions (Pakistan), check network traffic anomaly:
   - If the source IP equals destination IP, there's anomaly
   - number(Digit1, SourceIP), number(Digit2, DestIP)

The current coordinate of user: /* Coordinate */ ,Pay attention to the language used by locals.
Generate the complete anomaly detection rule using the appropriate logic and digit conversion.").

anomaly_detection(Digit1, Digit2, 0) :- \+ anomaly_detection(Digit1, Digit2, 1).
"""

def different_languange_test(MIXMNIST_train, MIXMNIST_test, train_set, test_set, train:bool, load_pretrained:bool, load_rule:bool, prompt_from_expert, save_to):
    # *** ================= *** =========== *** ================= *** 
    name = "language_{}_{}".format(save_to, 2)
    result_string = langda_solve("double_dc", 
                                 problog_string,
                                 model_name = "deepseek-reasoner",

                                prefix=f"{save_to}",
                                save_dir=current_dir,
                                load=load_rule,
                                langda_ext={"Coordinate":prompt_from_expert},
                                query_ext=query_ext,
                                 )

    print(result_string)
    network1 = MNIST_Net()
    network2 = MNIST_Net()
    network3 = MNIST_Net()
    network4 = MNIST_Net()

    net1 = Network(network1, "arabic_net", batching=True)
    net1.optimizer = torch.optim.Adam(network1.parameters(), lr=1e-3)
    net2 = Network(network2, "telugu_net", batching=True)
    net2.optimizer = torch.optim.Adam(network2.parameters(), lr=1e-3)
    net3 = Network(network3, "kannada_net", batching=True)
    net3.optimizer = torch.optim.Adam(network2.parameters(), lr=1e-3)
    net4 = Network(network4, "urdu_net", batching=True)
    net4.optimizer = torch.optim.Adam(network4.parameters(), lr=1e-3)

    model = Model(result_string, [net1,net2,net3,net4], load=False)
    model.set_engine(ExactEngine(model), cache=True)

    model.add_tensor_source("train", MIXMNIST_train)
    model.add_tensor_source("test", MIXMNIST_test)
    if load_pretrained:
        try:
            model.load_state("snapshot/{}.pth".format(name))
        except:
            print(f"No local model:{name} found, train it first.")
            pass

    if train:
        loader = DataLoader(train_set, 1, False)
        train = train_model(model, loader, 1, log_iter=100, profile=0)
        model.save_state("snapshot/{}.pth".format(name))
        train.logger.comment(dumps(model.get_hyperparameters()))
        print(f"\nFinish Training!")
        train.logger.comment(
            "Accuracy {}".format(get_confusion_matrix(model, test_set, verbose=1).accuracy())
        )
        train.logger.write_to_file("log/" + name)
    else:
        model.load_state("snapshot/{}.pth".format(name))
        model.eval()
        confusion_matrix = get_confusion_matrix(model, test_set, verbose=1)
        accuracy = confusion_matrix.accuracy()

        print(f"\nFinish Testing!")
        print(f"Accuracy: {accuracy:.4f}")

def operation(n: int, dataset: str, prefix: str, func: callable, seed=None, max_examples: Optional[int] = None):
    """Returns a dataset for binary addition
    
    :param max_examples: Maximum number of examples to generate (e.g., 2000)
    """
    return MNISTOperator(
        dataset_name=dataset,
        function_name="anomaly_detection",
        operator=func,
        size=n,
        arity=2,
        seed=seed,
        prefix=prefix,
        max_examples=max_examples 
    )

# =================== Real World Information =================== #
def machine(input:Iterable[int | bool]):
    return 1 if (input[0] >= 60 and input[1] <= 20) else 0
# Tensor Sources:
MIXMNIST_train = MIXMNIST(prefix="Arabic", subset="train") # prefix: load dataset: {prefix}_train_test.npz
MIXMNIST_test = MIXMNIST(prefix="Arabic", subset="test")
# Rules:
train_set = operation(2, "train", "Arabic", machine, seed=42)
test_set = operation(2, "test", "Arabic", machine, seed=42)

# Prompt:
save_to1 = "arabia"
prompt_from_gps = "(24.7136° N, 46.6753° E)"
# =================== Our Model =================== #
different_languange_test(MIXMNIST_train, MIXMNIST_test, train_set, test_set, train=True, load_pretrained=False, load_rule=True, prompt_from_expert=prompt_from_gps, save_to=save_to1)


# =================== Real World Information =================== #
def tank(input:Iterable[int | bool]):
    return 1 if (input[0] >= 75 or input[1] >= 15) else 0
# Tensor Sources:
MIXMNIST_train = MIXMNIST(prefix="Arabic", subset="train") # prefix: load dataset: {prefix}_train_test.npz
MIXMNIST_test = MIXMNIST(prefix="Arabic", subset="test")
# Rules:
train_set = operation(2, "train", "Arabic", tank, seed=42)
test_set = operation(2, "test", "Arabic", tank, seed=42)

# =================== Our Model =================== #
save_to2 = "iraq"
prompt_from_gps = "(33.3152° N, 44.3661° E)"
different_languange_test(MIXMNIST_train, MIXMNIST_test, train_set, test_set, train=True, load_pretrained=False, load_rule=True, prompt_from_expert=prompt_from_gps, save_to=save_to2)



# =================== Real World Information =================== #
def traffic(input:Iterable[int | bool]):
    return 1 if input[0] == input[1] else 0
# Tensor Sources:
MIXMNIST_train = MIXMNIST(prefix="Urdu", subset="train") # prefix: load dataset: {prefix}_train_test.npz
MIXMNIST_test = MIXMNIST(prefix="Urdu", subset="test")
# Rules:
train_set = operation(2, "train", "Urdu", traffic, seed=42)
test_set = operation(2, "test", "Urdu", traffic, seed=42)

# =================== Our Model =================== #
save_to5 = "pakistan"
prompt_from_gps = "(31.5204 N, 74.3587 E)"
different_languange_test(MIXMNIST_train, MIXMNIST_test, train_set, test_set, train=True, load_pretrained=False, load_rule=True, prompt_from_expert=prompt_from_gps, save_to=save_to5)