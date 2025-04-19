from setuptools import setup, find_packages

setup(
    name="Timothy-Gomoku",
    version="0.0.4",
    description="A simple Gomoku game powered by reinforcement learning.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Zeyu Xie",
    author_email="xie.zeyu20@gmail.com",
    url="https://github.com/Zeyu-Xie/Timothy-Gomoku",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
