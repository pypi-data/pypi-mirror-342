"""
This module contains the setup configuration for the italymusic package.
"""


from setuptools import find_packages, setup
from italymusic.utils import __version__


# Read the README file to use as the long description
with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

# Setup configuration
setup(
    name="italymusic",

    version=__version__,

    author="Italy Music",

    author_email="hetari4all@gmail.com",

    description="مكتبة لتحميل فيديوهات يوتيوب وتكاملها مع بوتات تليجرام",

    long_description=description,

    long_description_content_type="text/markdown",

    keywords=[
        "youtube",
        "download",
        "cli",
        "italymusic",
        "pytubefix",
        "pytube",
        "youtube-dl",
        "telegram",
        "pyrogram",
        "bot",
    ],

    license="MIT",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],

    include_package_data=True,

    python_requires=">=3.6",

    install_requires=[
        "pytubefix",
        "inquirer",
        "yaspin",
        "typer",
        "requests",
        "rich",
        "termcolor",
        "moviepy",
        "setuptools",
        "pyrogram",
        "tgcrypto",
        "asyncio",
    ],

    entry_points={
        "console_scripts": [
            "italymusic=italymusic:cli.app",
        ],
    },

    project_urls={
        "Author": "https://t.me/italy_5",
        "Homepage": "https://github.com/Hetari/pyutube",
        "Bug Tracker": "https://github.com/Hetari/pyutube/issues",
        "Source Code": "https://github.com/Hetari/pyutube",
        "Documentation": "https://github.com/Hetari/pyutube",
    },

    platforms=["Linux", "Windows", "MacOS"],
    packages=find_packages()
)
