from setuptools import setup, find_packages

setup(
    name="himosoft-sms-api-client",  # PyPI-friendly name
    version="1.0.0",  # Version starting point
    description="HIMOSOFT SMS API Client.",
    long_description=open("README.md").read(),  # Load the README file for PyPI
    long_description_content_type="text/markdown",  # Ensures correct Markdown rendering on PyPI
    author="HIMEL",
    author_email="python.package@himosoft.com.bd",
    url="https://github.com/swe-himelrana/himosoft-sms-client",  # Project repository URL
    license="MIT",
    packages=find_packages(exclude=["example", "tests"]),  # Exclude unwanted files/folders
    include_package_data=True,  # Include non-Python files listed in MANIFEST.in
    install_requires=[
        "requests>=2.25.1",  # Main package dependencies
        "urllib3>=1.26"
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],  # Development dependencies
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",  # Ensure compatibility with Python 3.6 and later
    keywords="himosoft sms api client",  # Keywords to improve searchability
)
