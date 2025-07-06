================================= 核 心 代 码 组 成 ==================================
====================================================================================

-----------------------
我非常想尝试将我的agent变成react agent, 但是苦于没有很好的prompt(我觉得更大的原因是不舍得之前的prompt...)
代码块的prolog改成problog
-----------------------


为了减少生成过多代码的情况, 将数据的格式修改为:
{
	HASH:1234ABCD,
	Code: "generated block..."
}

整合了v5.4的内容, 将项目变得更加“专业”和易于维护
已将功能组织成干净、可重复使用的组件（解析器、工具、节点等），这些组件可以独立维护和测试。

# 重大更新, 将所有内容进行了包装和划分, 现在代码变得易于管理(除了parser.py...我会之后尝试优化的...大概...)
现在结构如下:
- agent: GenerateNodes, EvaluateNodes, GeneralNodes 和一个额外的requirements_builder用来构建提示词的动态内容
- utils: models包含invoke_agent的各级逻辑
		 parser解析器
		 tools_for_agent, 我认为暂时用不到
		 tools最重要的部分, 包含了各种有用的小函数, 尝试让代码更加优雅^
- 主要层级:
config: 输出paths实例, 包含对路径的各种操作, 因为之前路径太让我抓狂了, 因此专门写了一个类
database: 用来管理已经生成的代码, 用来实现对langda对长期管理, 数据结构为{{"Hash1":"code content","Hash1":"code content",...}}
main_fullvision: 主要执行器, 执行工作流
state: 管理state类


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
