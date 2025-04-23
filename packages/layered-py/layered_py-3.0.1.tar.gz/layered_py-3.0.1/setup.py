from setuptools import setup, find_packages

setup(
    name="layered-py",
    version="3.0.1",
    description="A Python library for implementing layered architecture with services and dependency injection.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Malte Harms",
    author_email="mail@malteharms.dev",
    url="https://github.com/upNorthDev/LayeredPy",
    packages=find_packages(exclude=["tests*", "*.tests"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "layeredpy=cli.layeredpy:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="layered architecture, services, dependency injection, python",
    project_urls={
        "Bug Tracker": "https://github.com/upNorthDev/LayeredPy/issues",
        "Documentation": "https://github.com/upNorthDev/LayeredPy",
        "Source Code": "https://github.com/upNorthDev/LayeredPy",
    },
)
