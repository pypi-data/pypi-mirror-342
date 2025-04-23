from setuptools import setup

setup(
    name="nextstephr",
    version="0.1.0",
    packages=["nextstephr"],
    entry_points={
        "console_scripts": [
            "nextstephr = nextstephr.__main__:main"
        ]
    },
    author="nextstephr",
    description="CLI tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.6",
)
