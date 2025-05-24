=========================== Final version of the code ============================
==================================================================================
Test Files:
- main_test_brutal: Exceptions are exposed directly to the user, this is for debugging
- main_test_multi: Exceptions are captured in Summary, this is for performance testing


** In case these packages could not successfully installed:
!pip install langgraph
!pip install pydantic_settings
!pip install problog
!pip install langchain_groq
!pip install langchain_deepseek
!pip install langchain_community


*** requirements.txt ***

backoff==2.2.1
bpy==4.4.0
dd==0.6.0
fastapi==0.115.12
geojson==3.2.0
geopy==2.4.1
graphviz==0.20.3
groq==0.24.0
ipython==8.12.3
langchain==0.3.25
langchain_community==0.3.24
langchain_core==0.3.59
langchain_deepseek==0.1.3
langchain_groq==0.3.2
langchain_openai==0.3.16
langgraph==0.4.3
langserve==0.3.1
mathutils==3.3.0
matplotlib==3.7.2
nltk==3.9.1
numpy==2.2.5
overpy==0.7
pandas==2.2.3
Pillow==11.2.1
psipy==0.4.0
psutil==5.9.5
pydantic==2.11.4
pydantic_settings==2.9.1
pyeda==0.29.0
pyproj==3.7.1
PyQt4==4.11.4
PySDD==1.0.5
pyswip==0.3.2
pytest==8.3.5
python-dotenv==1.1.0
python-telegram-bot==22.0
python_igraph==0.11.8
retrying==1.3.4
scikit_learn==1.6.1
scipy==1.15.3
setuptools==67.7.2
Shapely==2.1.0
smopy==0.0.8
torch==2.4.0
torchvision==0.19.0
tqdm==4.65.0
typing_extensions==4.13.2
uvicorn==0.34.2


** .env content **

GNRT_DEEPSEEK_PROVIDER= deepseek
GNRT_DEEPSEEK_MODEL= deepseek-chat
GNRT_DEEPSEEK_API_KEY = fake-api-key
GNRT_DEEPSEEK_API_TYP = Bearer
GNRT_DEEPSEEK_API_VER = 2025-03-15

GNRT_GROQ_PROVIDER= groqcloud
GNRT_GROQ_MODEL = llama-3.1-8b-instant
GNRT_GROQ_API_KEY = fake-api-key
GNRT_GROQ_API_TYP = Bearer
GNRT_GROQ_API_VER = 2025-03-15

GNRT_OPENAI_PROVIDER= openai
GNRT_OPENAI_MODEL = gpt-4o-mini
GNRT_OPENAI_API_KEY = fake-api-key
GNRT_OPENAI_API_TYP = Bearer
GNRT_OPENAI_API_VER = 2025-00-00

TELEGRAM_BOT_TOKEN = 7802169894:AAFimcnhTr0mI8MK0icoSZ0_hOeIf445Rfs
TAVILY_API_KEY = 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

TEST_DEEPSEEK_API_KEY = sk-293f9d735260457583c3cbe0df475d4f
TEST_GROQ_API_KEY = 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

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=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
LANGSMITH_PROJECT=pr-mealy-yesterday-94