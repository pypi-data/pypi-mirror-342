from setuptools import setup, find_packages

setup(
    name="botococe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Nate Michalov",
    author_email="nmichalov@gmail.com",
    description="A minimal Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/natemichalov/botococe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 