from setuptools import setup, find_packages
from pathlib import Path
# Read the contents of the README file
readme_path = Path(__file__).parent / "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()
# Function to read requirements from a file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

# Get dependencies from requirements.txt
install_requires = parse_requirements('/Users/praveenkumarb/Desktop/scanvault/scanvault/requirements.txt')
# Define the setup configuration
setup(
    name = "scanvault",
    version = "0.0.2",
    author = "Praveenkumar B",
    install_requires = install_requires,
    packages = find_packages(),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license="Owned By Scan Vault",  # Specify your custom license here
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # Use a valid classifier for proprietary licenses
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6"
)