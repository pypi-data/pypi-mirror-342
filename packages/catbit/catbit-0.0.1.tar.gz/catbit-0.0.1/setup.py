
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="catbit",
    version="0.0.1",
    author="Inventocode",
    author_email="359148497@qq.com",
    description="帮助您将小猫板接入您的Python程序",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://idonothaveproject.url",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)