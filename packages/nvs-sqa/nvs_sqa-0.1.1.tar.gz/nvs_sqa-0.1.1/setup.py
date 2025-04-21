from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Define package data to include model checkpoints
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

# Include all files in checkpoints directory
extra_files = package_files('nvs_sqa/checkpoints')

setup(
    name="nvs_sqa",
    version="0.1.1",
    author="Vincent Qu",
    author_email="vincent.qu.cs@gmail.com",  
    description="No-reference quality assessment for neurally synthesized scenes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VincentQQu/nvs_sqa", 
    packages=find_packages(),
    package_data={"nvs_sqa": extra_files},
    include_package_data=True,
    install_requires=[
        "numpy",
        "torch>=1.7.0",
        "torchvision>=0.8.0",
        "scikit-learn",
        "pillow",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
