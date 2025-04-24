from setuptools import setup, find_packages


def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()


setup(
    name="lib_clockifybot",
    version="2.8.2",
    author="retr0err0r - veininvein",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
)
