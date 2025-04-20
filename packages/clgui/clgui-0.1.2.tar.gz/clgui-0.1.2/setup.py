from setuptools import setup, find_packages
with open('README.md', 'r') as f:
    long_description = f.read()


VERSION = '0.1.2'
DESCRIPTION = 'A command-line GUI for Python'

# Setting up
setup(
        name="clgui", 
        version=VERSION,
        author="TitusHM",
        author_email="contact@titushm.dev",
        description=DESCRIPTION,
        long_description=long_description,
        packages=find_packages(),
        install_requires=["colorama", "keyboard"],
        keywords=['cli gui', 'command line gui', "command line", "gui"],
        classifiers= [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    "Operating System :: OS Independent",
]
)