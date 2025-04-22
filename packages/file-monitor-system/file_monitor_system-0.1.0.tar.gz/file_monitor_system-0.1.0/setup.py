from setuptools import setup, find_packages

setup(
    name="file-monitor-system",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="Cross-platform real-time file monitoring and integrity verification",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-monitor",
    packages=find_packages(),
    install_requires=[
        "watchdog>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
