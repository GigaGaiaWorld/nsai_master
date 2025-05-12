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
        self.section_patterns = {
            'main_sections': {
                '4.1': 'Supported Prolog builtins',
                '4.2': 'ProbLog-specific builtins',
                '4.3': 'Available libraries'
            },
            'subsections': {
                '4.1': [
                    '4.1.1 Control predicates',
                    '4.1.2 Handling Undefined Procedures',
                    '4.1.3 Message Handling',
                    '4.1.4 Predicates on Terms',
                    '4.1.5 Predicates on Atoms',
                    '4.1.6 Predicates on Characters',
                    '4.1.7 Comparing Terms',
                    '4.1.8 Arithmetic',
                    '4.1.9 Remaining sections'
                ],
                '4.3': [
                    '4.3.1 Lists',
                    '4.3.2 Apply',
                    '4.3.3 Cut',
                    '4.3.4 Assert',
                    '4.3.5 Record',
                    '4.3.6 Aggregate',
                    '4.3.7 Collect',
                    '4.3.8 DB',
                    '4.3.9 Scope',
                    '4.3.10 String',
                    '4.3.11 NLP4PLP'
                ]
            }
        }
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
