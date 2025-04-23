import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pppmem",
    version="0.1.4",
    author="sugarkwork",
    description="Persisten Memory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sugarkwork/pmem",
    packages=setuptools.find_packages(),
    install_requires=[
        "aiosqlite",
        "setuptools",
    ],
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    keywords=["memory", "persistent", "async", "sqlite"],
    project_urls={
        "Homepage": "https://github.com/sugarkwork/pmem",
        "Repository": "https://github.com/sugarkwork/pmem",
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "tox>=4.0",
        ]
    },
)