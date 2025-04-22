# setup.py

from setuptools import setup, find_packages

setup(
    name='alqueda',
    version='0.1',
    description='A Python library with machine learning functions',
    author='Parinith',
    author_email='parinith99@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'torch',
        'tensorflow',
        'sklearn',
        'matplotlib',
        'keras',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
