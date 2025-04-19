from setuptools import setup, find_packages

# Function to read requirements from a file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

# Get dependencies from requirements.txt
install_requires = parse_requirements('requirements.txt')

# Read the long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='asfa',                # Name of your package
    version='1.1.1',            # Version
    packages=find_packages(),   # Automatically find packages in the 'your_package' directory
    install_requires=install_requires,  # List dependencies read from requirements.txt
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
