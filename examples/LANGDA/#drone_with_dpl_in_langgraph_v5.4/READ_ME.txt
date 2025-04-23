================================= 核 心 代 码 组 成 ==================================
====================================================================================
config.py -> file path
process_fullvision.py -> the langgraph code
_beautiful_addition.py => parser.py -> parser, parsing the langda predicate form, parsing the network string
state.py -> state class and other class
tool_v1.py -> tools, not used for this example
整合了v5.3的内容, 开始尝试使用mnist神经网络进行逻辑测试

为什么我们不直接使用prolog的内置PrologString进行解析, 而要自己定义呢?
- 我们本质上是在创建一个prompt, 它本质上并不是一个prolog代码(而且langda本身也不包含任何的“逻辑”), 直接套用会导致语法错误
- PrologString会忽略所有注释, 而这恰恰是我们prompt所需要的
- 我们要对代码进行处理和更改, 将它的格式变得更干净和清晰, 以方便llm的理解, 同时我们要处理直接替换langda项所导致的后续问题. 例如对它的注释应该如何处理
- 我们对lann项的处理同样无法通过普通的prolog内置parser或prgrammer实现
=======> 撤回我的话... 我感觉PrologString很靠谱, 能非常详细的解析各个项, 并且也和我们的语法兼容, 除了不能处理注释堪称完美.
=======> 上面的想法可以保留, 用以应答

test_parser.ipynb最后一个代码块, 新的parser, 之后测试...
=================================What is this example about==================================
============================================================================================= # 基于: examples/LANGDA/drone_with_langchain 的示例内容, 生成:

# 初始Langda格式:
# Langda谓词的格式: NET, LLM和其他参数...
valid_flight(X,T) :-
	langda(
    LOT:"[tool1,tool2,...]"
	NET:"[mnist_net1(0,1), mnist_net2(2,3)]", 
	LLM:"Please avoid the blue building"),

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


pip install pydantic-settings
