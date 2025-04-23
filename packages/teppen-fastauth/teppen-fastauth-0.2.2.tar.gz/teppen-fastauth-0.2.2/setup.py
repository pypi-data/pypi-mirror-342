from setuptools import setup, find_packages

setup(
    name="teppen-fastauth",
    version="0.2.2",
    author="Yasufumi Kamiyama",
    description="Authentication Library for FastAPI",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "PyJWT",
        "cryptography",
        "requests",
    ],
    license="MIT",
)
