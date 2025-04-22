from setuptools import setup, find_packages

setup(
    name="flagcapt",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
        'pycryptodome',
        'gmpy2',
        'libnum',
        'owiener',
        'beautifulsoup4',
        'lxml',
        'urllib3',
    ],
    description="A tool for solving cryptographic challenges in CTFs",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="1DH4M",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'flagcapt = flagcapt.__main__:main',
        ],
    },
)
