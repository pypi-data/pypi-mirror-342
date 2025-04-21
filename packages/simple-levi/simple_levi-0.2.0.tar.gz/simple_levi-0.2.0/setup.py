from setuptools import setup

setup(
    name="simple-levi",
    entry_points={
        "console_scripts": ["simple-levi = simple.server:main"]
    }
)