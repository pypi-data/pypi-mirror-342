from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ILpyTHERMO",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for accessing and processing ILThermo database data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ILpyTHERMO",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.25.0",
        "tqdm>=4.0.0",
    ],
)
