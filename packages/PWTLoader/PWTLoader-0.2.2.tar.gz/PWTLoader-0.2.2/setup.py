from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="PWTLoader",
    version="0.2.2",
    description="A lightweigh loader for data from Penn World Table datasets via Dataverse",
    author="Sarvesh Ingle",
    author_email="ingle.sarvesh1926@gmail.com",
    url="https://github.com/Sarv1926/notjustmacro",
    packages=find_packages(include=["PWTLoader"]),
   install_requires=[
    "pandas",
    "beautifulsoup4",
    "lxml",
    "requests"
],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="pwt, penn world table, economics, data loader, econometrics"
)