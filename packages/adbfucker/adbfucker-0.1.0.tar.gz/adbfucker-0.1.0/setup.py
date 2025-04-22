from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adbfucker",
    version="0.1.0",
    author="pedrogazil",
    author_email="pdrohenrique353@gmail.com",
    description="Tool for Android ADB automation with image recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrogazil/adbfucker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
    ],
) 