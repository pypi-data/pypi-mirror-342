from setuptools import setup, find_packages
from pathlib import Path

# خواندن محتوای README
root = Path(__file__).parent
long_description = (root / "README.md").read_text(encoding="utf-8")

setup(
    name="ancient-scripts-converter",
    version="1.0.2",  # همیشه نسخه را افزایش دهید
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
    package_dir={"": "ancient_scripts"},
    packages=find_packages(where="ancient_scripts"),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "deep-translator",
        
     
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
        "Documentation": "https://github.com/amirhossinpython/ancient-scripts/wiki",
    },
)