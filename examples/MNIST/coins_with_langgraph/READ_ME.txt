### I planned to apply langgraph to this example ###
pip install langgraph

add your own .env file in "src" folder, and add your api keys

======================================================
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