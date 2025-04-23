# setup.py
from setuptools import setup, find_packages

setup(
    name="vsa_explainer",
    version="0.1.0",
    description="Visualize and explain RDKit VSA descriptor contributions",
    author="Srijit Seal",
    author_email="seal@understanding.bio",
    license="MIT",
    packages=find_packages(),  # finds vsa_explainer/
    
    install_requires=[
        "numpy>=1.18",
        "matplotlib>=3.0",
        "rdkit",            # see rdkit install instructions for your platform
        "ipython",          # for IPython.display.SVG
    ],

    extras_require={
       "dev": ["pytest"],
    },
    tests_require=["pytest"],
    
    entry_points={
        "console_scripts": [
            "vsa-explain=vsa_explainer.explainer:visualize_vsa_contributions",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)