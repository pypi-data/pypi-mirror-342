#!/usr/bin/env python
from __future__ import absolute_import
from setuptools import setup, find_packages

# with open('README.rst') as readme_file:
#     readme = readme_file.read()

setup(
    name='kkauth-oidc',
    version='0.0.13',
    author='yliiii',
    author_email='',
    url='',
    description='OpenID Connect authentication provider for Sentry',
    long_description='',
    license='Apache 2.0',
    package_data={'': ['**/*.html']},
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'oidc = oidc.apps.Config',
        ],
    },
    python_requires='>=3.11, <4.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development',
    ],
    long_description_content_type='text/x-rst',
)
