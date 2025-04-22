from setuptools import setup, find_packages

setup(
    name="SPCC",  # Use a unique name, typically with hyphens
    version="0.1.0",
    description="A brief description of your package",
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)