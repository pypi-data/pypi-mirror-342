from setuptools import setup, find_packages

setup(
    name="datainsightx",
    version="1.0.1",
    author="Prakruthi Rao",
    author_email="prakruthirao040898@example.com",
    description="Automated KPI summary and trend analysis package for transactional datasets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
