# setup.py

from setuptools import setup, find_packages

setup(
    name='VanJr',
    version='0.1.0',
    description='VanJr: A lightweight Python library for streamlined data processing, EDA, and machine learning workflows.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abu Junior Vandi',
    author_email='abujuniorv@gmail.com',
    url='https://github.com/AbuJrVandi/VanJr',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'imbalanced-learn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.7',
)
