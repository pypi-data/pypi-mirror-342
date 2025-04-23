from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oe2pg",
    version="1.0.0",
    author="Benjamin Cance",
    author_email="canceb@gmail.com",
    description="Ready to use Progress to PostgreSQL database mirroring tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rowingdude/oe2pg",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
    ],
    python_requires=">=3.8",
    install_requires=[
        "psycopg2-binary>=2.9.6",
        "JayDeBeApi>=1.2.3",
        "xxhash>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "db-mirror=db_mirror.cli:main",
        ],
    },
    include_package_data=True,
)