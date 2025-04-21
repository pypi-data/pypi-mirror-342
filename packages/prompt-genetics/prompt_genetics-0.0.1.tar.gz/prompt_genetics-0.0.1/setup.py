from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read version from __init__.py
with open(os.path.join("prompt_genetics", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(" \"'")
            break

setup(
    name="prompt-genetics",
    version=version,
    description="Genetic algorithms for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oleg Sokolov",
    author_email="",  # Add your email if desired
    url="https://github.com/OlegSokolov/prompt-genetics",  # Update with the correct repository URL
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "prompt-genetics=prompt_genetics.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "flake8>=3.9.2",
            "isort>=5.9.1",
        ],
    },
    keywords="llm, prompt engineering, genetic algorithms, ai",
) 