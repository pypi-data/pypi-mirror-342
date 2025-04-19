from setuptools import setup, find_packages

setup(
    name="dcm-schememo",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "icalendar>=5.0.7"
    ],
    author="oboenikui",
    author_email="oboenikuitwitter@gmail.com",
    description="A Python library for docomo Schedule & Memo App backup data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oboenikui/dcm-schememo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)