from setuptools import setup, find_packages

setup(
    name="typer-try",  # Replace with your package name
    version="0.1.0",
    packages=find_packages(),
    py_modules=["main"],  # Your main script
    install_requires=[
        "typer[all]",  # Include Typer and its dependencies
    ],
    entry_points={
        "console_scripts": [
            "typer-try=main:app",  # Command to run your app
        ],
    },
    author="Tenzin Dorji",
    author_email="dtenzin.nov@gmail.com",
    description="A simple task manager CLI built with Typer.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/typer-try",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)