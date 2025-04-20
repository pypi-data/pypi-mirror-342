from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="IM-COOL-BOOY-FM",
    version="1.2.1",
    author="IM COOL BOOY",
    author_email="coolbooy@gmail.com",
    description="A colorful and powerful CLI tool to search, play, and manage your favorite radio stations worldwide.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["IM_COOL_BOOY_FM"],
    install_requires=[
        "requests>=2.25.0",
        "python-vlc>=3.0.1115",
        "colorama>=0.4.4",
    ],
    keywords=["FM"],
    entry_points={
        'console_scripts': [
           'IM-COOL-BOOY-FM=IM_COOL_BOOY_FM.main:main',
         ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
