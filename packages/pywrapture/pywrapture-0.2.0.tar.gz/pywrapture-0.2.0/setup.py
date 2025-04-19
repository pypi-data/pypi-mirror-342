# setup.py

from setuptools import setup, find_packages

setup(
    name='pywrapture', 
    version='0.2.0',
    author='matija',
    author_email='nmatija080@gmail.com',
    description='A simple greeting module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/n11kol11c/pywrapture',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
