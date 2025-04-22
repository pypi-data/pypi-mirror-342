from setuptools import setup, find_packages

setup(
    name="contribcast",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "langchain",
        "openai",
        "python-dotenv",
        "seaborn",
        "matplotlib",
    ],
    entry_points={
        'console_scripts': [
            'contribcast = contribcast.cli:main'
        ]
    },
)
