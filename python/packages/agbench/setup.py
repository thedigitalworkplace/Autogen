from setuptools import setup, find_packages

setup(
    name="agbench",  # Replace with your package name
    version="0.1.0",
    description="AutoGen Bench package",
    author="Nicholas (Project Contributor)",
    author_email="Oluwakayodenicholas1@gmail.com",
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
    python_requires=">=3.7",
)
