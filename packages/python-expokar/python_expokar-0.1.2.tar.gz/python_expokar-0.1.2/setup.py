from setuptools import setup, find_packages

setup(
    name="python-expokar",
    version="0.1.2",  # Updated version
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
    description="A collection of machine learning algorithm implementations with ready-to-use experiments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hellocoddes/python-expokar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers"
    ],
    python_requires=">=3.6",
    project_urls={
        "Bug Tracker": "https://github.com/hellocoddes/python-expokar/issues",
        "Documentation": "https://github.com/hellocoddes/python-expokar#readme",
    },
    keywords="machine learning, neural networks, logistic regression, SVM, experiments"
)