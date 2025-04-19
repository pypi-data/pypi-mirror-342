from setuptools import setup, find_packages

setup(
    name="cred-switcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "cred-switcher=cred_switcher.cli:main"
        ]
    },
)
