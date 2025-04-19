from setuptools import setup, find_packages

setup(
    name="MORPHO-toolkit",
    version="0.1.1-dev",
    author="EstesJorie",
    author_email="joe.tresise@aol.com",
    project_urls={"Source" : "https://github.com/EstesJorie/Morpho", "TrACKER" : "https://github.com/EstesJorie/Morpho/issues"},
    packages=find_packages(),  # This automatically includes all your packages
    install_requires=[
        'pandas==2.0.0',
        'glob2==0.7',
        'tqdm==4.62.0',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'scipy',
        'statsmodels',
        'icecream',
        'colorama>=0.4.4',
    ],
    extras_require={
        'dev': [
            'plotly',
            'xlrd',
        ],
        # 'logging' and 'json' are part of the Python standard library, so no need to list them
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',  # Specify the Python version you're using
        'License :: OSI Approved :: MIT License',  # License (if applicable)
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify the minimum Python version required
)