from setuptools import setup, find_packages

setup(
    name="gilman_rgi_to_csv",
    version="1.0",
    description="A tool to convert tab-delimited RGI files to CSV format",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/gilman_rgi_to_csv",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    entry_points={
        'console_scripts': [
            'gilman_rgi_to_csv=gilman_rgi_to_csv.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
