from setuptools import setup, find_packages

setup(
    name='bibas',
    version='0.1.1',
    description='Bayesian Networks Impact Factor Based on Analysis of Sensitivity',
    author='Gilad Erez',
    author_email='giladmatat@gmail.com',
    packages=find_packages(),
    install_requires=[
        "numpy<2.0",
        "pandas>=1.3",
        "matplotlib>=3.0",
        "seaborn>=0.11",
        "pgmpy>=0.1.22",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.7',
)