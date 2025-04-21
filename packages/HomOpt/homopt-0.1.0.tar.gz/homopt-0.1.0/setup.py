from setuptools import setup, find_packages
import pathlib

# 读取 README.md 内容作为长描述
here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="HomOpt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.6.0",  # 指定最低版本要求
    ],
    python_requires=">=3.6",  # 指定Python版本要求
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
    license="MIT",
    keywords="pytorch optimizer deep-learning",
    # 确保包含非Python文件（如果有）
    include_package_data=True,
)