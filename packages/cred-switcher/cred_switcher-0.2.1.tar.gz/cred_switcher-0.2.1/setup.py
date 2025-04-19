from setuptools import setup, find_packages

setup(
    name="cred-switcher",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "pyfiglet"
    ],
    entry_points={
        "console_scripts": [
            "cred-switcher=cred_switcher.cli:main"
        ]
    },

    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    description="A CLI tool to switch between Git and AWS credentials",
    author="Karizmattic876",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
