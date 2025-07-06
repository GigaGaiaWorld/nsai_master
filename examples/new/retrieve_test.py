from langda import langda_solve

model = """
langda(LLM:"the cleaner on plan yesterday was: Emily Johnson", LOT:"retrieve",FUP:"false").

query(ground_cleaned(true)).
"""

result = langda_solve('double_dc',model,'deepseek-chat')

# 数据库在util文件夹下, problog_docs.json8

"""
Invoking: `retriever_tool` with `{'query': 'F4DF5283'}`


Running retriever tool...
/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/langda/utils/vector_store_v4.py:26: LangChainDeprecationWarning: The class `OllamaEmbeddings` was deprecated in LangChain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the :class:`~langchain-ollama package and should be used instead. To use it run `pip install -U :class:`~langchain-ollama` and import as `from :class:`~langchain_ollama import OllamaEmbeddings``.
  self.embedding_function = OllamaEmbeddings(model="nomic-embed-text")
Vector store not found, creating new one...
Creating FAISS vector store...
Successfully loaded 3 items from /Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/langda/utils/problog_docs.json
Created 3 documents from JSON data
Vector store saved to /Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/langda/utils/vector_store/problog_docs
[(Document(id='a54fc440-17a1-4c47-bd2c-6d50dd65274b', metadata={'id': 'staff_status_2', 'title': 'On Leave Staff List', 'tags': ['status', 'leave'], 'keywords': ['on leave', 'vacation', 'sabbatical']}, page_content='1. Emily Johnson – Cleaner (On Annual Leave)\n2. Sarah Anderson – System Administrator (On Medical Leave)\n3. James Harris – Recruitment Specialist (On Parental Leave)\n4. Grace Hall – Regional Manager (On Sabbatical)\n5. Laura Adams – Security Team Leader (On Training Leave)'), 542.0251)]The retrieved information indicates that Emily Johnson, the cleaner, was on annual leave. Based on the requirements, the completed code should reflect this information. Here is the generated code:

```problog
% Information about the cleaner on plan yesterday
cleaner_on_leave("Emily Johnson").

% Query to check if the ground was cleaned
query(ground_cleaned(true)).
```
"""


"""
> Finished chain.
*** Generated New Code ***


% Fact: The cleaner on leave yesterday was Emily Johnson
cleaner_on_leave("Emily Johnson").

% Rule: The ground is cleaned if the cleaner is not on leave
ground_cleaned(true) :- \+ cleaner_on_leave(_).

% Query: Check if the ground is cleaned
query(ground_cleaned(true)).


Executing second chain: Code formatting...
processing _decide_next_gnrt... #current round: 2
### =========== ### current round: 2 ### =========== ###
### =========== processing evaluate_node =========== ###
cleaner_on_leave("Emily Johnson").
ground_cleaned(true) :- \+ cleaner_on_leave(_).
query(ground_cleaned(true)).
Running problog_test_tool...
 ------------- result_lines ------------- 
ground_cleaned(true) = 0.0000
Executing first chain: Code generation with tools...
"""