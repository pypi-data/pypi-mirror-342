from setuptools import setup, find_packages

setup(
    name="heygen-bot",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Selenium automation bot for Heygen",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/heygen-bot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
