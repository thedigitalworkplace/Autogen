from setuptools import setup, find_packages

setup(
    name="autogen_project", 
    version="0.1.0", 
    description="A project for AutoGen Studio functionality",
    long_description="This project provides advanced tools for AutoGen Studio integration.",  # Replace with your detailed description
    long_description_content_type="text/markdown",
    author="app.officio.com",  
    author_email=" ",  
    url="app.officio.work",  
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "openai",
        "azure-openai",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
