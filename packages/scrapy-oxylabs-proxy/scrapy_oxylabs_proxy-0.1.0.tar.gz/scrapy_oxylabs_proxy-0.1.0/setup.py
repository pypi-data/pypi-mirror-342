from setuptools import setup, find_packages

setup(
    name="scrapy-oxylabs-proxy",
    version="0.1.0",
    description="Scrapy middleware for Oxylabs Web Scraper API in proxy mode",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Abdul Nazar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Scrapy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
