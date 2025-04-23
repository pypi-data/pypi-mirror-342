from setuptools import setup, find_packages

setup(
    name="error_generator",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    author="Joshua Immanuel",
    author_email="joshua9@tamu.edu",
    description="A package for generating controlled errors in record linkage datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/joshuaimmanuel/error_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'generate_errors=error_generator.main:generate_errors',
        ],
    },
    include_package_data=True,
    package_data={
        'error_generator': ['data/*.csv'],
    },
) 