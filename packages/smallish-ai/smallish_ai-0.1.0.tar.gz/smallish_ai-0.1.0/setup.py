from setuptools import setup, find_packages

setup(
    name="smallish-ai",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "litellm",
        "dataclasses",
        "appdirs",
        "pylibmagic",
        "python-magic",
        "keyring",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "smai=smai.cli:main",
        ],
    },
    author="Sameer Ahuja",
    author_email="mail@sameerahuja.com",
    description="CLI tool for multimodal AI model calls, tool use, and more.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sam33r/smai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
