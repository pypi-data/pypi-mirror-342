from setuptools import setup, find_packages
from pathlib import Path

# خواندن خودکار README.md
root = Path(__file__).parent
long_description = (root / "README.md").read_text(encoding="utf-8")

setup(
    name="ancient_scripts",
    version="1.0.0",
    description="Comprehensive ancient scripts conversion toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amirhossinpython/ancient-scripts",
    author="Amir Hossein Khazaei",
    author_email="amirhossinpython03@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ancient scripts cuneiform hieroglyph pahlavi linguistics",
    packages=find_packages(include=["ancient_scripts", "ancient_scripts.*"]),
    package_dir={"": "."},
    package_data={
        "ancient_scripts": ["data/*.json"],
    },
    python_requires=">=3.8",
    install_requires=[
        "deep-translator>=1.11.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "twine>=4.0",
            "wheel>=0.38.0"
        ],
    },
    entry_points={
        "console_scripts": [
            "ancient-scripts=ancient_scripts.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/amirhossinpython/ancient-scripts/issues",
        "Source": "https://github.com/amirhossinpython/ancient-scripts",
    },
)