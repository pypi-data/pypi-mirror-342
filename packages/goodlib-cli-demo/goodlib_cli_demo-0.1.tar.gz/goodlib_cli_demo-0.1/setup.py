from setuptools import setup, find_packages

setup(
    name='goodlib-cli-demo',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'goodlib-cli=goodlib.__main__:main',
        ],
    },
)
