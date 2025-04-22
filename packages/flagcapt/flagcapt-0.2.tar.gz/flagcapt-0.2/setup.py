from setuptools import setup, find_packages

setup(
    name="flagcapt",  
    version="0.2",    
    packages=find_packages(),  
    install_requires=[],  
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
    python_requires='>=3.6',  # Minimum Python version
    entry_points={
        'console_scripts': [
            'flagcapt = flagcapt.__main__:main',
        ],
    },)
