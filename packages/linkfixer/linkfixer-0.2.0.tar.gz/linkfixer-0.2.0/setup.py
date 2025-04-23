
from setuptools import setup, find_packages

setup(
    name="linkfixer",
    version="0.2.0",
    description="A Python library to normalize, clean, and validate URLs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Renukumar R",
    author_email="renu2babu1110@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "idna>=2.5",
	
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.7',
)