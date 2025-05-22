================================= 核 心 代 码 组 成 ==================================
====================================================================================
config.py -> file path
parse.py -> parsing the langda predicate form, parsing the network string
process_fullvision.py -> the langgraph code
本来想创建process_fullvision和process_blockvision两个版本, 来测试“整体成成代码”和“分段生成代码”的性能, 不过现在要进行整体的调整, 所以搁置了
state.py -> state class and other class
tool_v1.py -> tools, not used for this example
 生成内容都存储在history文件夹下...
 提示词都在prompt文件夹下...

直接运行process_fullvision.py文件,将会运行call_gen_workflow函数

=================================What is this example about==================================
============================================================================================= # 基于: examples/LANGDA/drone_with_langchain 的示例内容, 生成:

# 初始Langda格式:
# Langda谓词的格式: NET, LLM和其他参数...
valid_flight() :-
	langda(X, T:"srase", ... ,
	NET:"[mnist_net1(0,1), mnist_net2(2,3)]", 
	LLM:"Please avoid the blue building"),

	other_rules(...), ...

# 处理后的Langda格式:
1. 自动生成代码部分
% ---------------------------- Network and Event Predicates ---------------------------- %
% NN Predicates:
nn(mnist_net1, [X], Y, [0, 1]) :: mnist_net1(X, Y).
nn(mnist_net2, [X], Y, [2, 3]) :: mnist_net2(X, Y).

% Event Predicate:
event(ID1, ID2, T) :-
    happenAt(X, Y, T),
    mnist_net1(X, ID1),
    mnist_net2(Y, ID2).

2. LLM生成代码部分
% % ---------------------------- LLM Generated Logic Codes ------------------------------- %
% Valid drone flight with neural networks and LLM information
valid_drone_flight(X) :-
    (langda(X,T), vlos(X));
    (can_return(X));
    langda(T).

3. 修改后的原代码:
valid_flight() :-
	langda(X, T),
	other_rules(...), ...


==========================Following are some install requirements============================
=============================================================================================
### I planned to apply langgraph to this example ###
pip install langgraph

add your own .env file in "src" folder, and add your api keys

LangServe: pip install --upgrade "langserve[all]"
LangChain CIL: pip install -U langchain-cli

langchain app new "myapp"

LangChain Serve:
# 安装 pipx，参考：https://pipx.pypa.io/stable/installation/
pip install pipx

# 加入到环境变量，需要重启 PyCharm
pipx ensurepath

# 安装 poetry，参考：https://python-poetry.org/docs/
pipx install poetry

# 安装 langchain-openai 库，例如：poetry add [package-name]
poetry add langchain
poetry add langchain-openai

可能需要:
conda install -c pytorch faiss-cpu
pip install sentence-transformers (huggingface embedding)

pip install -U psycopg psycopg-pool langgraph langgraph-checkpoint-postgres

注意:
train中的train_model函数参数顺序已被更改, 之前的run.py可能都无法直接运行

pip install overpy 
pip install smopy 
pip install geojson 
pip install shapely
pip install geopy
pip install pyproj