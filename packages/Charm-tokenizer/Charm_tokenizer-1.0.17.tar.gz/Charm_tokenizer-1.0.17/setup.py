from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='Charm_tokenizer',
    packages=find_packages(include=['Charm_tokenizer']),
    version='1.0.17',
    description='Official implementation of Charm tokenizer for ViTs',
    author='Fatemeh Behrad',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/FBehrad/Charm",
    author_email="fatemehbehrad@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["huggingface_hub", "timm==0.4.12", "transformers==4.36.0"],
    python_requires=">=3.8"
)