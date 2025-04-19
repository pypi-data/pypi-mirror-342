from setuptools import setup, find_packages

setup(
    name="pelipy",
    version="1.0.0",
    description="A Python wrapper for the Pelican Panel",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",  # Fixed missing comma
    author="uhalexz",
    url="https://github.com/uhalexz/pelipy",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",  # Fixed typo
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    keywords="pelican panel api wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/uhalexz/pelipy/issues",
        "Documentation": "https://github.com/uhalexz/pelipy#readme",
        "Source Code": "https://github.com/uhalexz/pelipy",
    },
)