from setuptools import setup

setup(
    name="pychetz",
    version="0.1.1",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "pychetz = main:main"
        ]
    },
    install_requires=[
        "urwid"
    ],
    author="Chetan Sanap",
    author_email="sanapchetan0718@gmail.com",  # Optional, replace or remove if you want
    description="Terminal-based Python code editor",
    long_description="A lightweight terminal-based Python editor with smart indentation, save dialog, and dark theme — built using Urwid.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
)
