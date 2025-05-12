import sys
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Type, ClassVar, Literal, Dict
from problog.program import PrologString
from problog import get_evaluatable, evaluator

from langchain.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.schema import Document

# from config import paths
from utils.vector_store_v3 import LangdaVectorStore

# project_root = paths.proj_dir
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

prolog_builtins = LangdaVectorStore("Prolog_builtins")
problog_builtins = LangdaVectorStore("Problog_builtins")
available_libraries = LangdaVectorStore("Available_libraries")
source_map = {
    "Prolog_builtins":prolog_builtins,
    "Problog_builtins":problog_builtins,
    "Available_libraries":available_libraries,
}
source_metadata_map = {
    "Prolog_builtins":prolog_builtins.section_metadata['4.1'],
    "Problog_builtins":problog_builtins.section_metadata['4.2'],
    "Available_libraries":available_libraries.section_metadata['4.3'],
}
# ======================================================================== #
#                                 BaseTools                                #
# ======================================================================== #

class SearchInput(BaseModel):
    query: str = Field(description="The search query to retrieve information.")

class CustomSearchTool(BaseTool):
    name:ClassVar[str] = "search_tool"
    description:ClassVar[str] = "Useful for searching additional information related to the current problem."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, 
             query: str, 
             run_manager: Optional[CallbackManagerForToolRun] = None) -> Optional[list[dict[str, Any]]]:
        """Use the search tool."""
        print(" Running search tool...")
        wrapped = TavilySearchResults(max_results=3)
        result = wrapped.ainvoke({"query": query})
        return result

    async def _arun(self, 
                    query: str, 
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> Optional[list[dict[str, Any]]]:
        """Async version of the tool - not implemented yet."""
        raise NotImplementedError("Async version not yet available")



class RetrieverInput(BaseModel):
    query: str = Field(description="The query string to search for in the knowledge base")

class RetrieverTool(BaseTool):
    name: ClassVar[str] = "retriever_tool"
    description: ClassVar[str] = f"""Useful for searching the ProbLog official documentation for syntax and predicate informations."""
    args_schema: Type[BaseModel] = RetrieverInput
    source_name: str

    def _run(self, 
            query: str, 
            run_manager: Optional[CallbackManagerForToolRun] = None) -> List[dict]:
        """
        Run the retriever tool to get relevant documents from the vector store.
        """
        print(" Running retriever tool...")
        # Perform similarity search
        results = {}
        try:
            vector_store = source_map[self.source_name]
            docs = vector_store.similarity_search(query, k=1)
            return self._format_results(docs, self.source_name)
        except:
            return {"error": f"Source not found: {self.source_name}"}
    
    def _format_results(self, docs:List[Document], source_name: str) -> List[dict]:
        """Format the search results with source information."""
        formatted = []
        for i, doc in enumerate(docs):
            formatted.append({
                "index": i,
                "source": source_name,
                "content": doc.page_content,
            })
        return formatted
    
class RetrieverToolFactory:
    """Factory class to create retriever tools for different vector stores"""
    
    @staticmethod
    def create_retriever_tool(source_name:str) -> RetrieverTool:
        """Create a retriever tool for Prolog builtins"""
        tool = RetrieverTool(
            name = f"{source_name}_retriever_tool",
            description = f"""Retrieve information about Prolog built-in predicates and functionality:
        {source_metadata_map[source_name]}""",
            source_name=source_name)

        return tool


class ProblogTestInput(BaseModel):
    model: str = Field(description="The full problog model string to evaluate")

class ProblogTestTool(BaseTool):
    name: ClassVar[str] = "problog_test_tool"
    description: ClassVar[str] = "Evaluate Problog models and queries to get probability results, you should use this tool whenever you are give a full problog code with 'query' term"
    args_schema: Type[BaseModel] = ProblogTestInput
    
    def _run(self, 
             model: str,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run the Problog evaluation tool."""
        try:
            result = []
            evaluatable:Type[evaluator.Evaluatable] = get_evaluatable().create_from(PrologString(model))
            results:(dict | Any) = evaluatable.evaluate()
            
            print("% ProbLog Inference Result：")
            for query_key, probability in results.items():
                result_line = f"{query_key} = {probability:.4f}"
                result.append(result_line)
                print(result_line)

            return "\n".join(result)
        except Exception as e:
            return f"Error evaluating Problog model: {str(e)}"
     
    async def _arun(self, 
                    model: str,
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Async version of the tool - not implemented yet."""
        raise NotImplementedError("Async version not yet available")


class FinishToolInput(BaseModel):
    output: str = Field(description="The full completed problog model string to output")

class FinishTool(BaseTool):
    name: ClassVar[str] = "finish_tool"
    description: ClassVar[str] = "Once you get the completed code, use this tool to return the final answer and end the chain"
    args_schema: Type[BaseModel] = FinishToolInput
    # return_direct: ClassVar[bool] = True  # End loop once called!!!

    def _run(self, 
             output:str,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        return output


# Dictionary mapping tool names to their respective classes
TOOL_REGISTRY = {
    "search_tool": CustomSearchTool,
    "Prolog_builtins_retriever_tool": RetrieverToolFactory.create_retriever_tool("Prolog_builtins"),
    "Problog_builtins_retriever_tool": RetrieverToolFactory.create_retriever_tool("Problog_builtins"),
    "Available_libraries_retriever_tool": RetrieverToolFactory.create_retriever_tool("Available_libraries"),
    "problog_test_tool": ProblogTestTool,
    "finish_tool": FinishTool,
}