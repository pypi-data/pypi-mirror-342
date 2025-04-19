from setuptools import setup

setup(
    name="netorca-sdk",
    packages=["netorca_sdk"],
    version="0.3.0",
    license="MIT",
    description="A package for interacting with the NetOrca API",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="Scott Rowlandson",
    author_email="scott@netautomate.org",
    url="https://gitlab.com/netorca_public/netorca_sdk/",
    keywords=["netorca", "orchestration", "netautomate"],
    install_requires=[
        "beautifultable",
        "ruamel.yaml",
        "requests",
        "gitpython",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
