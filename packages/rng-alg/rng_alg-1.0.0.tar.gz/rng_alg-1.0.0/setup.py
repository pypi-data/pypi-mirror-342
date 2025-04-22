from setuptools import setup, find_packages

setup(
    name='rng_alg',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "math",
        "random",
    ],
    author='Nickels',
    author_email="Nickels74130@outlook.fr",
    description='A package for random number generation algorithms like hexadecimal, pi, and advanced RNGs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)