from setuptools import setup, find_packages

setup(
    name="cat-stat-analysis",  # Name of your package
    version="0.1.0",  # Version number
    author="Your Name",  # Your name
    author_email="your.email@example.com",  # Your email
    description="A simple tool for analyzing relationships between categorical variables",
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cat-stat-analysis",  # Your GitHub URL or project homepage
    packages=find_packages(),  # Automatically finds the Python packages (directories with __init__.py)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Use the license you chose
        "Operating System :: OS Independent",
    ],
    install_requires=[  # Any external dependencies
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "fpdf",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)
