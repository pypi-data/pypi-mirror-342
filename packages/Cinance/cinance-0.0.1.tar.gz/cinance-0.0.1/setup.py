import os
from setuptools import setup, find_packages

# Đọc nội dung README.md
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="Cinance",
    version="0.0.1",
    description="Library with several features including [get_candle_data_about_minutes, get_candle_data_in_minute, get_candle_data_market, get_candle_data_in_range, get_symbol_list]",
    url="https://github.com/trgchinhh/LibraryCinance",
    author="Nguyen Truong Chinh",
    author_email="chinhcuber@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["requests>=2.25.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["get_candle_data_about_minutes", "get_candle_data_in_minute", "get_candle_data_market", "get_candle_data_in_range", "get_symbol_list"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
