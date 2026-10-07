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
        # 4.x crashes on Python 3.14 (custom tp_new metaclasses). 5.29.x does not.
        'protobuf==5.29.6',
        # storage 1.36 still imports pkg_resources, removed in setuptools 81+.
        'setuptools>=40.3.0,<81',
        # cgi was removed from the stdlib in 3.13; storage 1.36 still imports it.
        'legacy-cgi==2.6.4; python_version>="3.13"',
        'argparse==1.4.0'
    ],
    entry_points='''
        [console_scripts]
        target-cloud-storage=target_cloud_storage:main
    ''',
    packages=['target_cloud_storage']
)
