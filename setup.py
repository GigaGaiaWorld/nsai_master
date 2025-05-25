from setuptools import setup, find_packages

setup(
    name="langda",
    version="6.5.0",
    description="Language-Driven Agent for Probabilistic Logic Programming",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langgraph>=0.4.3",
        "pydantic>=2.11.4",
        "pydantic_settings>=2.9.1",
        "problog",
        "langchain>=0.3.25",
        "langchain_community>=0.3.24",
        "langchain_core>=0.3.59",
        "langchain_deepseek>=0.1.3",
        "python-dotenv>=1.1.0",
        "numpy",
        "matplotlib",
        "python-telegram-bot>=20.0",
    ],
    python_requires=">=3.8",
)