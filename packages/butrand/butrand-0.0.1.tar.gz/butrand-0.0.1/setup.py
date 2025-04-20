from setuptools import setup, find_packages

setup(
    name="butrand",
    version="0.0.1",
    author="Bùi Phong Phú",
    author_email="omerasutvailworkit@gmail.com",
    description="Fast and chaotic random number generator based on butterfly effect",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OmeraGod/butrand",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
