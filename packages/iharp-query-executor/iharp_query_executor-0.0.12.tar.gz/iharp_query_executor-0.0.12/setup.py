from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="iharp_query_executor",
    version="0.0.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "jupyter",
        "xarray",
        "netcdf4",
        "h5py",
        "dask[complete]",
        "pandas",
        "numpy",
        "plotly",
        "cdsapi",
        "shapely",
        "matplotlib",
        "geopandas",
        "requests",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iharp3/iharp-python-library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)