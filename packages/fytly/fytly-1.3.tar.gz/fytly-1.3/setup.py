from setuptools import setup
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="fytly",
    version="1.3",  # Update version as needed
    author="Aegletek",
    author_email="coe@aegletek.com",
    url="https://www.aegletek.com/",
    description="A grading component for keyword-based scoring for resumes",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    packages=["scorer"],  # Explicitly list your package
    package_dir={"": "."},  # Important for proper package discovery
    include_package_data=True,
    package_data={
        '': ['configs/*'],  # This ensures the configs folder is included in the package
        "scorer": ["*.txt", "*.md","*.properties"],
    },
    data_files=[
        ('fytly/configs', [
            'configs/app.properties',
            'configs/jd_keywords.txt',
            'configs/jfd_keywords.txt',
            'configs/pd_keywords.txt',
            'configs/pfd_keywords.txt',
        ])
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyPDF2",
        "python-docx",
        "pyspellchecker",
        "spacy",
        "nltk",
        "rapidfuzz",
    ],
)