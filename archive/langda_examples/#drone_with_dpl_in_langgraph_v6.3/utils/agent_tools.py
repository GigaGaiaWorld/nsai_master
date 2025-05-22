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
    # source: Literal["Prolog_builtins", "Problog_builtins", "Available_libraries", "All"] = Field(
    #     default="all", 
    #     description=f"""Search ProbLog knowledge base from multiple sources:

    #     {prolog_builtins.get_chapter_metadata}

    #     {problog_builtins.get_chapter_metadata}

    #     {available_libraries.get_chapter_metadata}
    #     """
    # )
    k: int = Field(default=3, description="Number of documents to retrieve")

class RetrieverTool(BaseTool):
    name: ClassVar[str] = "retriever_tool"
    description: ClassVar[str] = """Useful for searching the ProbLog official documentation for syntax and predicate informations,
use this tool when you need to:
    - Check if a Prolog predicate is supported in ProbLog
    - Find ProbLog-specific predicates and their syntax
    - Look up available libraries and their functions"""
    args_schema: Type[BaseModel] = RetrieverInput
    source_map: ClassVar[Dict[str,LangdaVectorStore]] = {
        "Prolog_builtins": prolog_builtins,
        "Problog_builtins": problog_builtins,
        "Available_libraries": available_libraries
    }

    def _run(self, 
            query: str, 
            # source: Literal["Prolog_builtins", "Problog_builtins", "Available_libraries", "All"] = "All",
            k: int = 3, 
            run_manager: Optional[CallbackManagerForToolRun] = None) -> List[dict]:
        """
        Run the retriever tool to get relevant documents from the vector store.
        """
        print(" Running retriever tool...")
        # Perform similarity search
        results = {}
        source = "all"
        if source == "all":
            # Search all sources
            for src_name, vector_store in self.source_map.items():
                docs = vector_store.similarity_search(query, k=k)
                results[src_name] = self._format_results(docs, src_name)

        else:
            # Search specific source
            if source in self.source_map:
                vector_store = self.source_map[source]
                docs = vector_store.similarity_search(query, k=k)
                results[source] = self._format_results(docs, source)
            else:
                return {"error": f"Unknown source: {source}"}

        return results
    
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
    
    async def _arun(self, 
            query: str, 
            k: int = 5, 
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> List[dict]:
        """Async version of the tool - not implemented yet."""
        raise NotImplementedError("Async version not yet available")


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

# Dictionary mapping tool names to their respective classes
TOOL_REGISTRY = {
    "search_tool": CustomSearchTool,
    "retriever_tool": RetrieverTool,
    "problog_test_tool": ProblogTestTool,
}