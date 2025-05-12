
from config import paths
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.schema import Document
from typing import List, Dict

class LangdaVectorStore:
    def __init__(self):
        self.problog_official_doc_path = paths.get_absproj_path("problog-readthedocs-io-en-latest.pdf")
        self.langda_db_dir = paths.get_absproj_path("faiss_langda_kb")
        self.index_name = "problog_readthedocs"
        self.index_file = self.langda_db_dir / f"{self.index_name}.faiss"
        self.embedding_function = OllamaEmbeddings(model="nomic-embed-text")
        self.index_content = """# ProbLog Chapter 4: Builtins and Libraries - Index

This chapter covers the built-in predicates and libraries available in ProbLog.

## 4.1 Supported and Unsupported Prolog builtins
Standard Prolog predicates supported or Unsupported by ProbLog (based on Yap Prolog).
- Control flow (true, fail, conjunction, disjunction, negation, cut, conditional statements, etc.)
- Term manipulation (var, atom, functor, arg, etc.)
- Arithmetic operations (+, -, *, /, and other mathematical functions)
- Term comparison (==, \\==, @<, sort, etc.)
- other prolog builtins...

## 4.2 ProbLog-specific builtins
Special predicates unique to ProbLog:
- subquery/2, subquery/3: Probabilistic queries
- debugprint/N, error/N: Debugging
- nocache/2: Cache control
- scope operations
- other problog specific builtins...

## 4.3 Available libraries
Additional functionality through libraries:
- Lists: Standard list operations (member, append, reverse)
- Aggregate: LDL++ style aggregation (sum, avg, min, max)
- DB: Database and CSV access
- Cut: Soft cut for ordered rules
- Assert: Dynamic fact management
- Scope: Theory management
- other libraries...
"""
        # Enhanced section metadata with descriptions and keywords
        self.section_metadata = {
            '4.1': {
                'title': 'Supported Prolog builtins',
                'description': 'Standard Prolog predicates supported by ProbLog based on Yap Prolog',
                'keywords': ['prolog', 'builtin', 'predicate', 'standard', 'yap'],
                'summary': 'This section covers standard Prolog predicates that are supported in ProbLog, including control predicates, term manipulation, arithmetic operations, and more.'
            },
            '4.2': {
                'title': 'ProbLog-specific builtins',
                'description': 'Special predicates unique to ProbLog for probabilistic logic programming',
                'keywords': ['problog', 'builtin', 'probabilistic', 'subquery', 'evidence', 'cache', 'scope'],
                'summary': 'This section covers ProbLog-specific predicates for handling probabilistic queries, evidence, debugging, and other features unique to probabilistic logic programming.'
            },
            '4.3': {
                'title': 'Available libraries',
                'description': 'Additional libraries that extend ProbLog functionality',
                'keywords': ['library', 'lists', 'aggregate', 'database', 'string', 'cut', 'assert'],
                'summary': 'This section describes various libraries available in ProbLog that provide additional functionality like list operations, aggregation, database access, and more.'
            }
        }
        
        self.subsection_metadata = {
            '4.1.1': {
                'title': 'Control predicates',
                'description': 'Flow control predicates like conjunction, disjunction, negation, ...',
                'keywords': ['control', 'flow', 'conjunction', 'disjunction', 'fail', 'true', 'false', 'not', 'call', 'once', 'cut', 'conditional statements'],
                'examples': ['P, Q', 'P; Q', 'true/0', 'fail/0', '\\+/1', 'call/1','!/0','P -> Q','P *-> Q']
            },
            '4.1.2': {
                'title': 'Handling Undefined Procedures',
                'description': 'How ProbLog handles undefined predicates',
                'keywords': ['undefined', 'procedure', 'unknown', 'fail'],
                'examples': ['unknown(fail)']
            },
            '4.1.3': {
                'title': 'Message Handling',
                'description': 'Message handling predicates (not supported)',
                'keywords': ['message handling'],
                'examples': []
            },
            '4.1.4': {
                'title': 'Predicates on Terms',
                'description': 'Predicates for term inspection and manipulation',
                'keywords': ['term', 'var', 'atom', 'compound', 'functor', 'arg', 'unification', 'is_list'],
                'examples': ['var/1', 'atom/1', 'compound/1', 'float/1', 'arg/3', 'X = Y', 'X \\= Y','is_list/1','T1 =@= T2']
            },
            '4.1.5': {
                'title': 'Predicates on Atoms',
                'description': 'Atom manipulation predicates (not supported)',
                'keywords': ['atom', 'not supported'],
                'examples': []
            },
            '4.1.6': {
                'title': 'Predicates on Characters',
                'description': 'Character manipulation predicates (not supported)',
                'keywords': ['character', 'not supported'],
                'examples': []
            },
            '4.1.7': {
                'title': 'Comparing Terms',
                'description': 'Term comparison predicates',
                'keywords': ['compare', 'equality', 'sort', 'length', 'ordering'],
                'examples': ['compare/3', 'X == Y', 'X \\== Y', 'X @< Y', 'sort/2', 'length/2']
            },
            '4.1.8': {
                'title': 'Arithmetic',
                'description': 'Arithmetic operations and mathematical functions',
                'keywords': ['arithmetic', 'math', 'calculation', 'plus', 'minus', 'multiply', 'divide', 'exp', 'log', 'sin', 'cos', 'sqrt'],
                'examples': ['X+Y', 'X-Y', 'X*Y', 'X/Y', 'X//Y','exp/1', 'log/1', 'sin/1', 'cos/1', 'X is Y','[X]','random/0']
            },
            '4.1.9': {
                'title': 'Remaining sections',
                'description': 'Other Prolog sections not supported',
                'keywords': ['remaining', 'not supported'],
                'examples': []
            },
            '4.3.1': {
                'title': 'Lists',
                'description': 'List manipulation predicates from SWI-Prolog',
                'keywords': ['list', 'member', 'append', 'select', 'reverse', 'sort', 'permutation'],
                'examples': ['member/2', 'append/3', 'select/3', 'reverse/2', 'permutation/2', 'flatten/2']
            },
            '4.3.2': {
                'title': 'Apply',
                'description': 'Higher-order predicates for list processing',
                'keywords': ['apply', 'maplist', 'foldl', 'include', 'exclude', 'partition'],
                'examples': ['maplist/2', 'maplist/3', 'foldl/4', 'include/3', 'exclude/3']
            },
            '4.3.3': {
                'title': 'Cut',
                'description': 'Soft cut implementation for ordered rulesets',
                'keywords': ['cut', 'soft cut', 'ordered', 'rules', 'indexed clauses'],
                'examples': ['cut/2']
            },
            '4.3.4': {
                'title': 'Assert',
                'description': 'Dynamic fact assertion and retraction',
                'keywords': ['assert', 'retract', 'dynamic', 'database', 'assertz', 'retractall'],
                'examples': ['assertz/1', 'retract/1', 'retractall/1']
            },
            '4.3.5': {
                'title': 'Record',
                'description': 'Non-backtrackable storage access',
                'keywords': ['record', 'storage', 'non-backtrackable', 'database'],
                'examples': ['recorda/2', 'recordz/2', 'recorded/2', 'erase/1']
            },
            '4.3.6': {
                'title': 'Aggregate',
                'description': 'LDL++ style aggregation operations',
                'keywords': ['aggregate', 'sum', 'avg', 'min', 'max', 'group by'],
                'examples': ['sum<X>', 'avg<X>', 'min<X>', 'max<X>']
            },
            '4.3.7': {
                'title': 'Collect',
                'description': 'Generalized aggregation with => operator',
                'keywords': ['collect', 'aggregation', 'group by', '=>'],
                'examples': ['(CODE) => GroupBy / AggFunc']
            },
            '4.3.8': {
                'title': 'DB',
                'description': 'SQLite database and CSV file access',
                'keywords': ['database', 'sqlite', 'csv', 'sql', 'data access'],
                'examples': ['sqlite_load/1', 'sqlite_csv/2']
            },
            '4.3.9': {
                'title': 'Scope',
                'description': 'Managing multiple ProbLog theories with scopes',
                'keywords': ['scope', 'theory', 'namespace', 'union', 'conjunction'],
                'examples': ['scope(1):predicate', 'scope1:X; scope2:X']
            },
            '4.3.10': {
                'title': 'String',
                'description': 'String manipulation predicates',
                'keywords': ['string', 'manipulation', 'text processing'],
                'examples': []
            },
            '4.3.11': {
                'title': 'NLP4PLP',
                'description': 'Library for representing and solving probability questions',
                'keywords': ['nlp', 'natural language', 'probability', 'questions'],
                'examples': []
            }
        }


    def _create_index_document(self) -> Document:
        """Create an index document that helps agents understand the structure"""
        return Document(
            page_content=self.index_content,
            metadata={
                'chapter': '4',
                'type': 'index',
                'title': 'Chapter 4 Index',
                'description': 'Overview of ProbLog builtins and libraries'
            }
        )
    
    def _create_structured_documents(self, documents: List[Document]) -> List[Document]:
        """Create structured documents with enhanced metadata"""

        return structured_docs
    
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
