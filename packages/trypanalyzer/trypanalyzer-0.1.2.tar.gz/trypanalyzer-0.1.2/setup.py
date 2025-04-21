from setuptools import setup, find_packages

setup(
    name="trypanalyzer",
    version="0.1.2",
    author="Julian Peters",
    description="A package for analyzing trypanosome motion and structure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abissmo/trypanalyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scipy", 
        "h5py",
        "scikit-learn",
    ],
)