from setuptools import setup, find_packages

setup(
    name="datacleancraft",
    version="0.1.0",
    description="End-to-end data ingestion, cleaning, anomaly detection, and export tool.",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "pandas",
        "numpy",
        "torch",
        "spacy",
        "openai",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "datacleancraft=datacleancraft.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
