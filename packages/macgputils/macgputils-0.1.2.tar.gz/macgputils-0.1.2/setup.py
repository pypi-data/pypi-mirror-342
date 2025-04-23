from setuptools import setup, find_packages

setup(
    name="macgputils",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        # List of dependencies, for example:
        # "numpy>=1.19",
    ],
    author="Your Name",
    author_email="your-email@example.com",
    description="A package to fetch GPU stats on macOS using powermetrics",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/macgputils",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the Python version your package supports
)
