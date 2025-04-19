from setuptools import setup, find_packages

setup(
    name="openfoam-postprocess",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.19.0",
    ],
    author="Mactone Hsieh",
    author_email="mactonehsieh@gmail.com",
    description="OpenFOAM 數據處理與可視化工具",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mactonehsieh/openfoam-postprocess",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "openfoam-postprocess=src.main:main",
        ],
    },
) 