from setuptools import setup, find_packages

setup(
    name='nlp_package_mitb_2025',
    version='0.1.0',
    description='A Python package for various NLP utilities.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'nltk>=3.6.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
