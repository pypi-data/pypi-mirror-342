# setup.py
from setuptools import setup, find_packages

setup(
    name="gitgpt",
    version="0.1.0",
    description="AI-powered Git commit assistant using GPT and git diff",
    author="Nolan Manteufel",
    packages=find_packages(),
    install_requires=["openai"],
    entry_points={
        'console_scripts': [
            'gitgpt = gitgpt.cli:interactive_commit_flow',
        ],
    },
    python_requires='>=3.7',
)
