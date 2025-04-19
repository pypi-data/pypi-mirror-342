from setuptools import setup, find_packages

setup(
    name="sachin_chess_utils",
    version="0.1.1",
    author="Sachin Chauhan Infocusp",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.11.0'
    ],
    entry_points={
        'console_scripts': [
            'sachin_hello = sachin_chess_utils:hello'
        ]
    }
)
