from setuptools import find_packages, setup

setup(
    name="fastapi-project-creator",
    version="0.2.2",  # Increment the version number
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "create-fastapi-app=fastapi_project_creator.main:main"  # Make sure package name is correct
        ],
    },
    install_requires=[],
    author="Raihan Hidayatullah Djunaedi",
    author_email="raihanhd.dev@gmail.com",
    description="CLI tool to generate FastAPI project structure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raihanhd12/fastapi-project-creator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
