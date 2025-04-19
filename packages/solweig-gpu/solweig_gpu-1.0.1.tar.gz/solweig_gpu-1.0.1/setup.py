from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solweig-gpu",
    version="1.0.1",
    author="Harsh Kamath, Naveen Sudharsan",
    author_email="harsh.kamath@utexas.edu, naveens@utexas.edu",
    description="GPU-accelerated SOLWEIG model for urban thermal comfort simulation",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/nvnsudharsan/SOLWEIG-GPU",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch",
        "numpy",
        "scipy",
        "pandas",
        "netCDF4",
        "pytz",
        "shapely",
        "timezonefinder",
        "gdal",
        "xarray",
        "tqdm",
        "PyQt5",
    ],
    entry_points={
        'console_scripts': [
            'thermal_comfort=solweig_gpu.cli:main',
            'solweig_gpu=solweig_gpu.solweig_gpu_gui:main',
        ],
    },
)
