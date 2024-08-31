from setuptools import setup, find_packages

setup(
    name="upinfo78",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    author="frieda",
    author_email="www778878net@189.cn",
    description="UpInfo78的Python实现",
    long_description="""
    UpInfo78是一个用于处理特定信息的Python库。
    它提供了与TypeScript版本相同的功能,可以轻松地在Python项目中使用。
    
    主要特性:
    - 功能1
    - 功能2
    - 功能3
    
    详细使用说明请参阅项目文档。
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/upinfo78",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)