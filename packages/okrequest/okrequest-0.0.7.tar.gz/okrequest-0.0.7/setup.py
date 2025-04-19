from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="okrequest",
    version="0.0.7",
    packages=find_packages(),
    package_data={
        'okrequest': ['*.dll', '*.so', '*.h', 'libs/*'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="一个类似 requests 的 HTTP 客户端库",
    author="",
    author_email="",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # 在这里添加你的依赖
    ]
)