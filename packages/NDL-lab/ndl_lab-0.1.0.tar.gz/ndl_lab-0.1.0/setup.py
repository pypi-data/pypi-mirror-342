from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))
with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='NDL_lab',
    version='0.1.0',
    author='Nicolas De La Torre',
    description='Neural Networks and Deep Learning Test',
    long_description=long_description, long_description_content_type='text/markdown',packages=find_packages(exclude=['tests']),auto_discover_packages=True,install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'matplotlib>=3.4.0',
        'pandas>=1.2.0',
        'seaborn>=0.11.0',
        'scikit-learn>=0.24.0',
        'tensorflow>=2.5.0',
        'keras>=2.4.3'
    ]
)