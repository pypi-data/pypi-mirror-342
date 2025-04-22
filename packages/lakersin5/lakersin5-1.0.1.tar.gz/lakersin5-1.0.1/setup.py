from setuptools import setup, find_packages

setup(
    name='lakersin5',
    version='0.1.1',
    packages=find_packages(),
    package_data={
        'lakersin5': ['cheatsheet/*.txt'],  # Include the cheatsheet text files
    },
    include_package_data=True,
    install_requires=[
        'pycryptodome',  # Automatically install pycryptodome
    ],
)