from setuptools import setup, find_packages

setup(
    name="python-plus-tools",
    version="1.3.0a3",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "toml>=0.10", "indently-decorators>=1.0,<=1.1", "cryptography>=3.4", "imgfit>=0.3", "colorama>=0.1", "deprecated>=1", 
        "numpy>=1.14", "matplotlib>=3.4","torch>=2", "pandas>=2", "requests>=2.27"
        ],
    python_requires=">=3.7",
    author="xystudio",
    author_email="173288240@qq.com",
    description="For the expansion of python content, it covers science, debugging and other fields.",
    long_description=open("README-PYPI.md",encoding="utf-8").read(),
    license="MIT",
    url="https://github.com/xystudio889/pyplus",
    include_package_data=True, 
    entry_points={
        "console_scripts": [
            "pyplus = pyplus.__init__:main",
        ]
    }, 
    extras_require={
    "dev": [],
    "test": [
        "flake8", 
        "mypy"
    ],
    "build": [
        "build", 
        "setuptools", 
        "twine"
    ]
    }
)
