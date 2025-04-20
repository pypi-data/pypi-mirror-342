from setuptools import setup, find_packages

setup(
    name="apikcmd",
    version="0.1.0",
    author="KC",
    description="A simple command interface for REST API CRUD operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apikcmd",  # Change this if needed
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
