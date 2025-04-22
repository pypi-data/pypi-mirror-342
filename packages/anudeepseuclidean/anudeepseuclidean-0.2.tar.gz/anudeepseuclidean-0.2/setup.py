from setuptools import setup, find_packages

setup(
    name='anudeepseuclidean',
    version='0.2',  # Increment version
    description='A simple Euclidean distance calculator',
    author='Anudeep Errabelly',
    author_email='errabellyanudeep@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
