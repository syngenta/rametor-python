import os
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='syngenta_digital_dbv',
    version=os.getenv('CIRCLE_TAG'),
    url='https://github.com/syngenta-digital/package-python-dbv.git',
    author='Paul Cruse III, Technical Lead, Syngenta Digital',
    author_email='paul.cruse@syngenta.com',
    description='A DRY multi-database migration tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.0',
    install_requires=[
        'aws-psycopg2',
        'boto3',
        'pymongo'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
