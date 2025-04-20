from setuptools import setup, find_packages

setup(
    name="gangthisisatestbro",
    version="0.1.1",
    packages=find_packages(include=["gangthisisatestbro", "gangthisisatestbro.*"]),
    description="A sample Python package",
    author="Gang This Is A Test Bro",
    author_email="idklololo@gmail.com",
    url="https://github.com/yourusername/gangthisisatestbro",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 