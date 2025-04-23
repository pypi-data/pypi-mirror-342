from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="buildsnap",
    version="0.1.0",
    description="Snap together Python package builds and init",
    author="imAnesYT",
    author_email="imanesyt.contact@gmail.com",
    url="https://github.com/imAnesYT/buildsnap",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "buildsnap=buildsnap.cli:cli",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)