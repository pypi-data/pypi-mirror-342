from setuptools import setup, find_packages

setup(
    name='otailab',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'networkx>=2.0',
        'matplotlib>=3.0',
        'numpy>=1.19.0',
        'scipy>=1.6.0',
        'sympy>=1.8'
    ],
    author='Tamilselvan A K',
    author_email='aktamil13@gmail.com',
    description='A Python package for Operations Research and Optimization Algorithms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TamilSelvan7708/otailab.git',
classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],
    python_requires='>=3.6',
)
