================================= 核 心 代 码 组 成 ==================================
====================================================================================

整合了v5.4的内容, 将项目变得更加“专业”和易于维护

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
通过数据库长期的管理:
from utils import _compute_random_md5, _compute_short_md5
a = _compute_random_md5() # 随机哈希
b = _compute_short_md5("hhhsadasd") # 静态哈希
c = a + b 
print(c[:8])
print(c[8:])
区分“强制更新”和“保证不动”的情况

The dictonary key for database maintaince: (16 bit)
Front 8 bit: (force update flag 1 bit) + (random hash 7 bit)
Last  8 bit: (static md5 hash based on content)

{
 'F36C44002BE63E73': 'langda(LLM:"hello")', 
 'T13BDD4S7A9BCDA3': 'langda(LLM:"world")',
}
langda的新项: ”FUP“:bool决定是否强制更新
FUP: true  = (true  -> true) : 始终更新, 使用随机哈希     T 13BDD4S 7A9BCDA3 -> T TU23D4S 7A9BCDA3: update 
		   & (false -> true) : 突然开始更新, 		     F 13BDD4S 7A9BCDA3 -> T TU23D4S 7A9BCDA3

FUP: false = (false -> false): 始终不更新, 使用静态哈希    T 13BDD4S 7A9BCDA3 -> T TU23D4S 7A9BCDA3
		   & (true  -> false): 突然不更新, 保留上一个状态  T 13BDD4S 7A9BCDA3 -> T TU23D4S 7A9BCDA3


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
