from setuptools import setup, find_packages

install_requires = [
    "matplotlib==3.9.0",
    "matplotlib-inline==0.1.6",
    "matplotx==0.3.10",
    "numpy==1.26.4",
    "pandas==2.2.1",
]

setup(
    name="ctoi",
    version="0.4",
    packages=find_packages(include=["."]),
    py_modules=["visualizer"],
    include_package_data=True,
)
