#!/usr/bin/env python

from setuptools import setup

setup(
    name='target-cloud-storage',
    version='1.0.0',
    description='hotglue target for exporting data to Google Cloud Storage',
    author='hotglue',
    url='https://hotglue.xyz',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['target_cloud_storage'],
    install_requires=[
        'google-cloud-storage==1.36.2',
        'argparse==1.4.0'
    ],
    entry_points='''
        [console_scripts]
        target-cloud-storage=target_cloud_storage:main
    ''',
    packages=['target_cloud_storage']
)
