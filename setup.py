from setuptools import setup

setup(
    # Application name:
    name="storebench",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Quentin Guilloteau",
    author_email="Quentin.Guilloteau@univ-grenoble-alpes.fr",

    # Packages
    packages=["app"],

    # Include additional files into the package
    # include_package_data=True,
    entry_points={
        'console_scripts': ['storebench=app.storebench:main'],
    },


    #
    license="LICENSE",
    description="Store Bench",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
    ],
    
    include_package_data=True,
)
