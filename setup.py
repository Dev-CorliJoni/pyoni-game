from setuptools import setup, find_packages


def load_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


setup(
    name="pyoni-game",
    version="0.1",
    packages=find_packages(),
    install_requires=load_requirements("requirements.txt"),
    author="Dev-CorliJoni",
    author_email="",
    description="Framework for building 2d games",
    url="https://github.com/Dev-CorliJoni/pyoni-game",
)