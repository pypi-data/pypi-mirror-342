from setuptools import setup, find_packages

setup(
    name="daplexer",  # Updated package name
    version="3.2.4",
    description="A Python package tools for Scientific Computing, Machine Learning and manipulating graphs and networks",
    author="73",
    author_email="73@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "daplexer": ["data/*.txt"],  # Updated to match new package name
    },
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)