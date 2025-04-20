from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Ensure the output directory exists
os.makedirs(os.path.join("cli", "output"), exist_ok=True)

setup(
    name="prompt-surfer",
    version="0.1.3",
    author="Jaden Tripp",
    author_email="jadenitripp@gmail.com",
    description="A retro-styled terminal application for generating AI prompts across multiple creative platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jadentripp/prompt-surfer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'openai>=1.3.0',
        'openai-agents>=0.0.11',
        'python-dotenv>=1.0.0',
        'rich>=13.7.0',
        'questionary>=2.0.0',
        'tiktoken>=0.5.1',
        'pyperclip>=1.8.2',
        'aiohttp>=3.9.1',
        'asyncio>=3.4.3'
    ],
    entry_points={
        'console_scripts': [
            'prompt-surfer=cli.src.cli:main',
        ],
    },
    package_data={
        'cli': ['prompts/*.txt'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
        "Topic :: Artistic Software",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    keywords="ai, prompt, midjourney, suno, udio, openai, cli, terminal, tui",
)