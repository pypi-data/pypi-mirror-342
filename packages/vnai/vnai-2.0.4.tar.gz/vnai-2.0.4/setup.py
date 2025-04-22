from setuptools import setup, find_packages

long_description = (
    "System resource management and "
    "performance optimization toolkit"
)

setup(
    name="vnai",
    version='2.0.4',
    description="System optimization and resource management toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vnstock HQ",
    author_email="support@vnstocks.com",
    url="https://github.com/vnstock-hq/initialization/new/main",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "psutil>=5.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
        ],
    },
    license="MIT",
)