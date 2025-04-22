from setuptools import setup, find_packages

setup(
    name="snoopish_demo",            # must be globally unique on PyPI
    version="0.0.1",
    description="Demo PyPI package linking to Snoopish website",
    url="https://snoopish.com",      # <-- your homepage backlink
    author="Snoopish",
    packages=find_packages(),        # points at the empty package below
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
