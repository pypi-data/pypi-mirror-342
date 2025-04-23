from setuptools import setup
import os

setup(
    name='pychetz',
    version='0.1',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'pychetz = main:main',
        ],
    },
    install_requires=[
        'urwid',
    ],
    author='Chetan Sanap',
    description='A lightweight terminal-based Python code editor',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
