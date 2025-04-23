from setuptools import setup, find_packages

setup(
    name="python-expokar",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
        "matplotlib>=3.3.0",
        "pandas>=1.2.0",
        "seaborn>=0.11.0"
    ],
    author="exposable",
    author_email="expose@mailla.com",
    description="A collection of machine learning algorithm implementations including Logistic Regression, SVM, Neural Networks, and PCA",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hellocoddes/python-expokar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.6",
)