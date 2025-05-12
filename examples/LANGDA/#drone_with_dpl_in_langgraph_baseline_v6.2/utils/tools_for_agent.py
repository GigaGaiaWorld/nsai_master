import os
import sys
import torch
import asyncio
from typing import Any, Callable, List, Optional, Tuple, Type, ClassVar
from mnist import MNIST_Net, MNIST_Classifier, neural_predicate
from prob_ec_testing import test
import config as cf

from pydantic import BaseModel, Field
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
#                              Basic Functions                             #
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
    try:
        if isinstance(problog_files, list):
            for problog_file in problog_files:
                with open(problog_file) as f:
                    problog_string += f.read()
                    problog_string += '\n\n'
        else:
            with open(problog_files) as f:
                problog_string += f.read()
                problog_string += '\n\n'
    except Exception as e:
        print("Error by add_files_to function:", e)
    return problog_string
    

def my_test(net_str_list:List[Tuple[str,int]], 
            test_data:str, 
            problog_files:str, problog_test_files:List[str], load_model:Model) -> list:

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
            problog_files:str, problog_train_files:List[str], problog_test_files:List[str]) -> dict:

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
    # net_str_list: List[Tuple[str, int]] = Field(description="A list of tuples where each tuple contains a network name and its corresponding number of outputs.")
    problog_files:str = Field(description="The name of the generated model.")
    # load_model: str = Field(description="The name of the pre-trained model.")
    bias_test: bool = Field(description="Test with biased data or original data")

class Train_Input(BaseModel):
    net_str_list: List[Tuple[str, int]] = Field(description="A list of tuples where each tuple contains a network name and its corresponding number of outputs.")


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
        # net_str_list: List[Tuple[str, int]], load_model: Model,
        problog_files: str, 
        bias_test:bool,
        # run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> list:
        """Use the tool."""
        print("trying to call the test tool...")
        try:
            test_data = cf.RESULT_TEST_BIASED if bias_test else cf.RESULT_TEST_ORIGIN
            # problog_files = cf.LOGIC_COMPLEX
            problog_file_path = problog_files
            problog_test_files = cf.HAPPEN_TEST_BIASED if bias_test else cf.HAPPEN_TEST_ORIGIN
            problog_model_file = cf.MODEL_PATH

            result = my_test([("mnist_net1",2), ("mnist_net2",2)], 
                             test_data, 
                             problog_file_path, 
                             problog_test_files, 
                             problog_model_file)
            print("================= get the result =================")
            return str(result)
        except Exception as e:
            print(f"================= custom_test error {e} =================")
            return str(e)

    async def _arun(
        self,
        bias_test:bool,
    ) -> list:
        """Use the tool asynchronously."""
        print("============ Use the async test tool =============")
        # try:
        #     test_data = cf.RESULT_TEST_BIASED if bias_test else cf.RESULT_TEST_ORIGIN
        #     problog_test_files = cf.HAPPEN_TEST_BIASED if bias_test else cf.HAPPEN_TEST_ORIGIN

        #     result = await asyncio.to_thread(my_test, net_str_list, test_data, problog_files, problog_test_files, load_model)
        #     return str(result)
        # except Exception as e:
        #     print(f"custom_test error {e}")
        raise TypeError("============ async version not yet available ============")


class CustomTrainTool(BaseTool):
    name:ClassVar[str] = "custom_train"
    description:ClassVar[str] = "Tool to train a Problog model using provided training data, test data, and network configurations."
    args_schema: Type[BaseModel] = Train_Input
    return_direct:ClassVar[bool] = True

    def _run(
        self,
        net_str_list: List[Tuple[str, int]],
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool."""
        print("trying to call the train tool...")
        try:
            test_data = cf.RESULT_TEST_ORIGIN
            training_data = cf.RESULT_TRAIN_ORIGIN
            problog_test_files = cf.HAPPEN_TEST_ORIGIN
            problog_train_files = cf.HAPPEN_TRAIN_ORIGIN
            problog_files = cf.LOGIC_ORIGIN

            result = my_train(net_str_list, training_data, test_data, problog_files, problog_train_files, problog_test_files)
            return str(result)
        except Exception as e:
            print(f"custom_train error {e}")

    async def _arun(
        self,
        net_str_list: List[Tuple[str, int]],
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool asynchronously."""
        try:
            test_data = cf.RESULT_TEST_ORIGIN
            training_data = cf.RESULT_TRAIN_ORIGIN
            problog_test_files = cf.HAPPEN_TEST_ORIGIN
            problog_train_files = cf.HAPPEN_TRAIN_ORIGIN
            problog_files = cf.LOGIC_ORIGIN

            result = await asyncio.to_thread(my_train, net_str_list, training_data, test_data, problog_files, problog_train_files, problog_test_files)
            return str(result)
        except Exception as e:
            print(f"custom_train error {e}")






class Dummy_Test_Input(BaseModel):
    bias_test: bool = Field(description="Test with biased data or original data")

class DummyTestTool(BaseTool):
    name:ClassVar[str] = "custom_test"
    description:ClassVar[str] = "Tool to test a Problog model using provided test data and network configuration."
    args_schema: Type[BaseModel] = Dummy_Test_Input
    return_direct:ClassVar[bool] = True

    # In your CustomTestTool class
    def _run(
        self,
        bias_test: bool,
    ) -> list:
        """Use the tool."""
        print(f"============ Tool received parameter: bias_test={bias_test} =============")
        try:
            if bias_test:
                result = "bias test result: This is the result of a biased test"
            else:
                result = "non-biased test result: This is the result of a non-biased test"
            print(f"Tool returning result: {result}")
            return result
        except Exception as e:
            print(f"custom_test error {e}")
            return f"Error: {str(e)}"