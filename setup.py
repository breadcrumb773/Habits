from setuptools import setup, find_packages

setup(
    name="fastapi_test",
    version="0.1.0",
    description="Add your description here",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.116.1",
        "httpie>=3.2.4",
        "httpx>=0.28.1",
        "requests>=2.32.5",
        "uvicorn>=0.35.0",
    ],
    python_requires=">=3.11",
)
