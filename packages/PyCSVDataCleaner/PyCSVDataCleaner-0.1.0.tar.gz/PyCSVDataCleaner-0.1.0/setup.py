from setuptools import setup, find_packages

setup(
    name='PyCSVDataCleaner',
    version='0.1.0',
    description='A lightweight Python package to clean CSV files',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Md. Ismiel Hossen Abir',
    author_email='ismielabir1971@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)