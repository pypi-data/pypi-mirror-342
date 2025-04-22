from setuptools import setup, find_packages

setup(
    name="doc_quality",
    version="0.1.0",
    description="A Python library for evaluating documentation quality using 14 metrics.",
    author="Your Name",
    author_email="sristy.sumana@usask.ca",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "spacy",
        "textstat",
        "pandas",
        "beautifulsoup4",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
