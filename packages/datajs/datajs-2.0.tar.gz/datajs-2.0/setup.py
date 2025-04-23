import setuptools

with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name="datajs",
    version="2.0",
    author="Minegamer",
    description="A library to make working with JSON files simpler",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/Minegamer2024/datajs",
    packages=setuptools.find_packages(where="src"),
    package_dir={"":"src"},
    python_requires=">=3.8,<=3.12.9",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="python, json, js, datajs"
)