from setuptools import setup, find_packages

setup(
    name='otailab',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'networkx>=2.0',
        'matplotlib>=3.0'
    ],
)
