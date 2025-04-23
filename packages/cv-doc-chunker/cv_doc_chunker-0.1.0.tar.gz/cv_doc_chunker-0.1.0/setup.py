import setuptools
import os

# Function to read the contents of requirements.txt
def read_requirements(file_path="requirements.txt"):
    # Filter out empty lines and comments
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Function to read the long description from README.md
def read_long_description(file_path="README.md"):
    # Check if README exists
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Skipping long description.")
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}. Error: {e}. Skipping long description.")
        return ""

setuptools.setup(
    name="cv-doc-chunker",
    version="0.1.0",
    author="Your Name / Team Name",
    author_email="your.email@example.com",
    description="A tool for parsing PDF document layouts and chunking content.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cv-doc-parser",
    license="MIT",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "cv-chunker=cv_doc_chunker.cli:main",
        ],
    },
    python_requires=">=3.8",
    keywords="pdf, ocr, parsing, document analysis, layout detection, chunking, cv",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Text Processing :: Indexing",
    ],
)
