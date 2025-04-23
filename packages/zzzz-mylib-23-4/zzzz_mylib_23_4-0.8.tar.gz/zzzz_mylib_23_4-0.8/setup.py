from setuptools import setup, find_packages

with open("README.md", mode="r") as file:
    description = file.read()

MYLIB_NAME = "zzzz_mylib_23_4"
__version__ = "0.8"  # Chỉnh phiên bản ở đây sau mỗi lần sửa code

REQUIRED_LIBS = [
    "tensorflow==2.18.0",
    "keras-cv==0.9.0",
    "pandas",
    "numpy==1.27.0",
    "matplotlib",
    "scikit-learn==1.3.0",
    "python-box==6.0.2",
    "pyYAML",
    "types-PyYAML",
    "plotly",
    "seaborn",
    "xgboost",
    "lightgbm",
]

setup(
    name=MYLIB_NAME,
    version=__version__,
    packages=find_packages(),
    install_requires=REQUIRED_LIBS,
    long_description=description,
    long_description_content_type="text/markdown",
)
