from setuptools import setup, find_packages

setup(
    name="aws_access_key_id",  # Name of your package on PyPI
    version="1.2",             # Initial version
    author="Nag Medida",
    author_email="nagwww@gmail.com",
    description="Extract AWS account ID and resource type from an AWS access key ID.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nagwww/aws_access_key_id",  # Update with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

