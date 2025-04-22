from setuptools import setup, find_packages

setup(
    name='pypql',
    version='0.1.1',
    description='A lightweight Pythonic interface for PostgreSQL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jake B',
    author_email='your@email.com',
    url='https://github.com/yourusername/pypql',
    packages=find_packages(),
    install_requires=[
        'asyncpg',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)