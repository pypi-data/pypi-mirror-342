from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="qrcodex",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Advanced QR Code Generator with Multiple Data Types Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qrcodex",
    packages=find_packages(),
    install_requires=[
        'qrcode >=7.4',
        'pillow >=9.0',
        'python-magic >=0.4.24'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'qrcodex=qrcodex.cli:main',
        ],
    },
    include_package_data=True,
)