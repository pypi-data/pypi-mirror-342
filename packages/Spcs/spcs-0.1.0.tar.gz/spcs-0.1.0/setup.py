from setuptools import setup, find_packages

setup(
    name="Spcs",  # Use a unique name, typically with hyphens
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)