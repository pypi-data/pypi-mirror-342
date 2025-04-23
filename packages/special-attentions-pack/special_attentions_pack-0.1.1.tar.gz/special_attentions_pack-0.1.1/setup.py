from setuptools import setup, find_packages
import pathlib

# 当前文件夹
HERE = pathlib.Path(__file__).parent

# 读取 README 作为 long_description
LONG_DESC = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="special-attentions-pack",           # 发布到 PyPI 的包名（需唯一）
    version="0.1.1",
    author="Your Name",
    author_email="you@example.com",
    description="A collection of sparse attention mechanisms",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/special_attentions",  # 项目主页
    license="MIT",
    packages=find_packages(where="src"),      # 找到 src 下的包
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 在这里列出运行时依赖
        # e.g. "torch>=1.8.0", "numpy"
    ],
    extras_require={
        "dev": ["pytest", "flake8"],
    },
)
