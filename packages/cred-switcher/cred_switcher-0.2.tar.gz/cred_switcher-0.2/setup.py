from setuptools import setup, find_packages

setup(
    name="cred-switcher",
    version="0.2",
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
)
