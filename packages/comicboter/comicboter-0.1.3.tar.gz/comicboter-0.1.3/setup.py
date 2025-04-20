from setuptools import setup, find_packages

setup(
    name="comicboter",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'ncatbot',
        'jmcomic',
        'requests',
        'pyyaml',
        'configparser',
    ],
    entry_points={
        'console_scripts': [
            'comicboter = bot:main',
        ],
    },
    author="ycssbc",
    author_email="ycssbc@126.com",
    description="A QQ bot for managing and downloading comics",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NapNeko/NapCatQQ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="Apache License 2.0",
    license_files=("LICENSE",),
    python_requires='>=3.6',
)