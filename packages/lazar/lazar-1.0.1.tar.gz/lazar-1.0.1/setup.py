from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lazar",
    version="1.0.1",
    author="xycan",
    author_email="eternals.tolong@gmail.com",
    description="A lightweight but powerful alternative to NumPy and Transformers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eternals-Satya/lazar",
    packages=find_packages(include=["lazar", "lazar.*"]),  # <--- fix ini
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="numpy alternative, lightweight, array processing",
)
