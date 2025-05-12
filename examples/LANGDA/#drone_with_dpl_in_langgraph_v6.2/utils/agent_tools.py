import sys
from typing import Any, List, Optional, Type, ClassVar

from config import paths
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import OllamaEmbeddings

# ======================================================================== #
#                                Retriever                                 #
# ======================================================================== #
class LangdaVectorStore:
    def __init__(self):
        self.problog_official_doc_path = paths.get_absproj_path("problog-readthedocs-io-en-latest.pdf")
        self.langda_db_dir = paths.get_absproj_path("faiss_langda_kb")
        self.index_name="problog_readthedocs"
        self.index_file = self.langda_db_dir / f"{self.index_name}.faiss"

        self.embedding_function = OllamaEmbeddings(model="nomic-embed-text")

    @property
    def vs(self) -> FAISS:
        """
        Get vector storage object
        """
        if self.index_file.exists():
            vector_store = FAISS.load_local(
                self.langda_db_dir,
                self.embedding_function,
                allow_dangerous_deserialization=True
            )

        else:
            loader = PyMuPDFLoader(self.problog_official_doc_path)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)

            vector_store = FAISS.from_documents(chunks, self.embedding_function)
            vector_store.save_local(self.langda_db_dir, index_name="problog_readthedocs")
        return vector_store

    def similarity_search(self, query: str, k: int = 5):
        """
        Perform similarity search on the local vector library.
        args:
            query: search query text
            k: number of results to return

        returns:
            document list
        """
        return self.vs.similarity_search(query, k=k)


from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
project_root = paths.proj_dir
if project_root not in sys.path:
    sys.path.insert(0, project_root)

vectorstore_object = LangdaVectorStore()
# ======================================================================== #
#                                 BaseTools                                #
# ======================================================================== #
class SearchInput(BaseModel):
    query: str = Field(description="The search query to retrieve information.")

class CustomSearchTool(BaseTool):
    name:ClassVar[str] = "search_tool"
    description:ClassVar[str] = "Useful for searching additional information related to the current problem."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Optional[list[dict[str, Any]]]:
        """Use the search tool."""
        print(" Running search tool...")
        wrapped = TavilySearchResults(max_results=2)
        result = wrapped.ainvoke({"query": query})
        return result

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> Optional[list[dict[str, Any]]]:
        """Use the tool asynchronously."""
        print(" Running async search tool...")
        try:
            wrapped = TavilySearchResults(max_results=2)
            result = await wrapped.ainvoke({"query": query})
            return result
        except Exception as e:
            print(f"custom_test error {e}")


class RetrieverInput(BaseModel):
    query: str = Field(description="The query string to search for in the knowledge base")
    k: int = Field(default=5, description="Number of documents to retrieve")

class RetrieverTool(BaseTool):
    name: ClassVar[str] = "retriever_tool"
    description: ClassVar[str] = "Useful for searching the ProbLog documentation for information and examples."
    args_schema: Type[BaseModel] = RetrieverInput
        
    def _run(self, 
            query: str, 
            k: int = 5, 
            run_manager: Optional[CallbackManagerForToolRun] = None) -> List[dict]:
        """
        Run the retriever tool to get relevant documents from the vector store.
        """
        print(" Running retriever tool...")
        # Perform similarity search
        docs = vectorstore_object.vs.similarity_search(query, k=k)
        
        # Format the results
        results = []
        for i, doc in enumerate(docs):
            # Extract page number if it exists
            page_number = doc.metadata.get('page', None)
            
            results.append({
                "index": i,
                "page": page_number,  # Include the actual page number
                "content": doc.page_content,
                "metadata": doc.metadata
            })
            
        return results
    
    async def _arun(self, 
            query: str, 
            k: int = 5, 
            run_manager: Optional[CallbackManagerForToolRun] = None) -> List[dict]:
        """Async version of _run"""
        print(" Running async retriever tool...")
        # For simplicity, we're just calling the sync version
        return self._run(query=query, k=k)

# Dictionary mapping tool names to their respective classes
TOOL_REGISTRY = {
    "search_tool": CustomSearchTool,
    "retriever_tool": RetrieverTool
}