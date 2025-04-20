from setuptools import setup, find_packages

setup(
    name="PyBioQuanta",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  
    author="Md. Ismiel Hossen Abir",
    author_email="ismielabir1971@gmail.com",
    description="PyBioQuanta: A small bioinformatics toolkit with 6 essential tools.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires='>=3.6',
)