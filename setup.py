import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysymreplace",
    version="0.0.1",
    author="Patrick Jennings",
    author_email="patrick@jenningsga.com",
    description="A command line utility for managing symbolic links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickjennings/pysymreplace",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['pysymreplace = pysymreplace:main']
    },
)
