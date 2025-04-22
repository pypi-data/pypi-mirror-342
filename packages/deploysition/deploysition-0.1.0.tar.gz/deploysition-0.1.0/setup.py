from setuptools import setup

setup(
    name="deploysition",
    version="0.1.0",
    packages=["deploysition"],
    entry_points={
        "console_scripts": [
            "deploysition = deploysition.__main__:main"
        ]
    },
    author="Deploysition",
    description="CLI tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.6",
)
