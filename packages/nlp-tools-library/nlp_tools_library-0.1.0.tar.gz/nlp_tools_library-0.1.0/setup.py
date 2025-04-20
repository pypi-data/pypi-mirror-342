from setuptools import setup, find_packages

setup(
    name="nlp_tools_library",  # Choose your package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nltk>=3.6.0",
        "spacy>=3.0.0",
        "scikit-learn>=0.24.0",
        "hmmlearn>=0.2.5",
        "regex>=2021.8.3",
    ],
    author="Vedant Raikar",
    author_email="vedantraikar117@gmail.com",
    description="A comprehensive NLP toolkit based on lab exercises",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
