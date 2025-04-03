import os
import sys
from typing import Any, Callable, List, Optional, Tuple, Type, ClassVar
from pydantic import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# ======================================================================== #
#                                 BaseTool                                 #
# ======================================================================== #
from pydantic import BaseModel, Field
from typing import List, Tuple

class Test_Input(BaseModel):
    bias_test: bool = Field(description="Test with biased data or original data")

class CustomTestTool(BaseTool):
    name:ClassVar[str] = "custom_test"
    description:ClassVar[str] = "Tool to test a Problog model using provided test data and network configuration."
    args_schema: Type[BaseModel] = Test_Input
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


# ======================================================================== #
#                                  TOOLS                                   #
# ======================================================================== #




