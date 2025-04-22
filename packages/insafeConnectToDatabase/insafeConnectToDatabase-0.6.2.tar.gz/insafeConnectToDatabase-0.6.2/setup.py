# setup.py
import shutil
import os
from setuptools import setup, find_packages

# Remove previous 'dist' and 'build' directories
for directory in ['dist', 'build']:
    if os.path.exists(directory):
        shutil.rmtree(directory)

def read_version():
    with open("VERSION","r") as version_file:
        return version_file.read().strip()


def increment_version(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"

def write_version(version):
    with open("VERSION", "w") as version_file:
        version_file.write(version)


current_version = read_version()
new_version = increment_version(current_version)
write_version(new_version)

setup(
    name="insafeConnectToDatabase",  # Name of your package
    version="0.6.2",  # Version of your package
    description="A utility to determine the type of permit based on ID",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="khaled.jabari",
    author_email="khaled.jabari@cntxt.com",
    url="https://github.com",  # Replace with your repo link
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # Automatically find all packages
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        'insafeConnectToDatabase': ['cloud-sql-proxy', 'cloud-sql-proxy-linux'],  # Include the script
    },
    install_requires=[
        "pydantic>=1.10.0",  # Add any dependencies here
        "psycopg2",  # Add psycopg2 dependency
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
