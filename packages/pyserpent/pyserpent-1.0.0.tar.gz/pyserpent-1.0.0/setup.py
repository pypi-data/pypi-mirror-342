from setuptools import setup, find_packages

setup(
    name='pyserpent',
    version='1.0.0',
    description='Pure Python implementation of the Serpent block cipher with CBC mode and PKCS#7 padding',
    author='svvqt',
    author_email='your_email@example.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)