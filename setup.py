from setuptools import setup, find_packages


def load_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


setup(
    name="pyoni-game",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pyoni-game=pyonigame._cli_commands:main",
        ],
    },
    install_requires=load_requirements("requirements.txt"),
    include_package_data=True,
    package_data={
        'pyonigame': ['resources/*'],
    },
    author="Dev-CorliJoni",
    author_email="",
    description="Framework for building 2d games",
    url="https://github.com/Dev-CorliJoni/pyoni-game",
)
