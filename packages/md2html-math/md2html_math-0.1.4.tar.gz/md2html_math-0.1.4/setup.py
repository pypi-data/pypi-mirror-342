from setuptools import setup, find_packages

setup(
    name="md2html-math",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "markdown>=3.8",
        "jinja2>=3.0.0",
        "python-markdown-math>=0.8",
        "pymdown-extensions>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=6.0.0",
        ],
    },
    python_requires=">=3.11",
    author="Marco Allanda",
    author_email="marcoallanda@gmail.com",
    description="A markdown to HTML converter with LaTeX math support and beautiful styling",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marcoallanda01/md2html-math",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "md2html-math=md2html.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "md2html": ["templates/*.html"],
    },
) 
