import os
import sys
import torch
from typing import Any, Callable, List, Optional, Tuple, Type, ClassVar
from mnist import MNIST_Net, MNIST_Classifier, neural_predicate
from prob_ec_testing import test

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain_community.tools.tavily_search import TavilySearchResults

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.deepprobcep.model import Model
from src.deepprobcep.train import train_model
from src.deepprobcep.data_loader import load
from src.deepprobcep.optimizer import Optimizer
from src.deepprobcep.network import Network
# ======================================================================== #
#                             Basic Functions                              #
# ======================================================================== #
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
def add_files_to(problog_files, problog_string):
    for problog_file in problog_files:
        with open(problog_file) as f:
            problog_string += f.read()
            problog_string += '\n\n'

    return problog_string
    

def my_test(net_str_list:List[Tuple[str,int]], 
            test_data:str, 
            problog_files:List[str], problog_test_files:List[str], load_model:Model=()) -> list:

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


# ======================================================================== #
#                                 BaseTool                                 #
# ======================================================================== #
from pydantic import BaseModel, Field
from typing import List, Tuple


class SearchInput(BaseModel):
    query: str = Field(description="The search query to retrieve information.")

class Test_Input(BaseModel):
    net_str_list: List[Tuple[str, int]] = Field(description="A list of tuples where each tuple contains a network name and its corresponding integer parameter.")
    test_data: str = Field(description="The test data content or the file path of the test queries.")
    problog_files: List[str] = Field(description="A list of file paths for the base Problog configuration files.")
    problog_test_files: List[str] = Field(description="A list of file paths for the Problog configuration files used specifically for testing.")
    load_model: str = Field(description="The path to pre-trained model.")

class Train_Input(BaseModel):
    net_str_list: List[Tuple[str, int]] = Field(description="A list of tuples where each tuple contains a network name and its corresponding integer parameter.")
    training_data: str = Field(description="The training data content or the file path of the training queries.")
    test_data: str = Field(description="The test data content or the file path of the test queries.")
    problog_files: List[str] = Field(description="A list of file paths for the base Problog configuration files.")
    problog_train_files: List[str] = Field(description="A list of file paths for the Problog configuration files used for training.")
    problog_test_files: List[str] = Field(description="A list of file paths for the Problog configuration files used for testing.")


class CustomSearchTool(BaseTool):
    name:ClassVar[str] = "custom_search"
    description:ClassVar[str] = "Useful for searching additional information related to the current problem."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Optional[list[dict[str, Any]]]:
        """Use the tool."""
        wrapped = TavilySearchResults(max_results=2)
        result = wrapped.ainvoke({"query": query})
        return result

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> Optional[list[dict[str, Any]]]:
        """Use the tool asynchronously."""
        try:
            wrapped = TavilySearchResults(max_results=2)
            result = await wrapped.ainvoke({"query": query})
            return result
        except Exception as e:
            print(f"custom_test error {e}")


class CustomTestTool(BaseTool):
    name:ClassVar[str] = "custom_test"
    description:ClassVar[str] = "Tool to test a Problog model using provided test data and network configuration."
    args_schema: Type[BaseModel] = Test_Input
    return_direct:ClassVar[bool] = True

    def _run(
        self,
        net_str_list: List[Tuple[str, int]], test_data: str,
        problog_files: List[str], problog_test_files: List[str], load_model: Model,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> list:
        """Use the tool."""
        try:
            result = my_test(net_str_list, test_data, problog_files, problog_test_files, load_model)
            return str(result)
        except Exception as e:
            print(f"custom_test error {e}")

    async def _arun(
        self,
        net_str_list: List[Tuple[str, int]], test_data: str,
        problog_files: List[str], problog_test_files: List[str], load_model: Model,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> list:
        """Use the tool asynchronously."""
        try:
            result = my_test(net_str_list, test_data, problog_files, problog_test_files, load_model)
            return str(result)
        except Exception as e:
            print(f"custom_test error {e}")


class CustomTrainTool(BaseTool):
    name:ClassVar[str] = "custom_train"
    description:ClassVar[str] = "Tool to train a Problog model using provided training data, test data, and network configurations."
    args_schema: Type[BaseModel] = Train_Input
    return_direct:ClassVar[bool] = True

    def _run(
        self,
        net_str_list: List[Tuple[str, int]],
        training_data: str,
        test_data: str,
        problog_files: List[str],
        problog_train_files: List[str],
        problog_test_files: List[str],
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool."""
        try:
            result = my_train(net_str_list, training_data, test_data, problog_files, problog_train_files, problog_test_files)
            return str(result)
        except Exception as e:
            print(f"custom_test error {e}")

    async def _arun(
        self,
        net_str_list: List[Tuple[str, int]],
        training_data: str,
        test_data: str,
        problog_files: List[str],
        problog_train_files: List[str],
        problog_test_files: List[str],
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool asynchronously."""
        try:
            result = my_train(net_str_list, training_data, test_data, problog_files, problog_train_files, problog_test_files)
            return str(result)
        except Exception as e:
            print(f"custom_test error {e}")


# ======================================================================== #
#                                  TOOLS                                   #
# ======================================================================== #
search_tool = CustomSearchTool()
my_test_tool = CustomTestTool()
my_train_tool = CustomTrainTool()

TOOLS: List[BaseTool] = [
    search_tool,
    my_test_tool,
    my_train_tool,
]



