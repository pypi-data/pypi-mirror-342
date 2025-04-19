from setuptools import setup, find_packages

setup(
    name="kivai_sdk",
    version="0.1.0",
    description="SDK for validating Kivai protocol commands",
    author="OpenKivai Community",
    packages=find_packages(),
    install_requires=["jsonschema"],
    keywords=["kivai", "validator", "jsonschema", "iot", "commands"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
