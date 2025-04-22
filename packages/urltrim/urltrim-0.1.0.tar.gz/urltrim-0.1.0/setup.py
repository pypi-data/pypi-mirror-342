from setuptools import setup, find_packages

setup(
    name="urltrim",
    version="0.1.0",
    author="PRANEETH KUMAR UDDARAJU",
    author_email="upraneeth24@gmail.com",
    description="A Python library to trim long URLs in code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/upraneethkumar/urltrim",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)