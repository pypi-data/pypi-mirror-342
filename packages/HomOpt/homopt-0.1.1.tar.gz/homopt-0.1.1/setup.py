from setuptools import setup, find_packages
import pathlib

# Read the README.md file for the long description
here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="HomOpt",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "torch>=1.6.0",  # Specify minimum required version of torch
    ],
    python_requires=">=3.6",  # Specify Python version requirement
    author="Yu Zhou",
    author_email="yu_zhou@yeah.net",
    description="A collection of homogeneous optimizers for PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yu-Zhou-1/HomOpt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    license="MIT",  # Specify the license type here
    keywords="pytorch optimizer deep-learning",
    include_package_data=True,  # Ensure non-Python files are included
)
