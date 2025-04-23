#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='touchtext',
    description='Markup Markdown, Stack up markdown files with `!INCLUDE` directives.',
    version='0.0.1',
    author='Torchtext Team, Hai Liang W.',
    author_email='hailiang.hl.wang@gmail.com',
    url='https://github.com/hailiang-wang/transformer-pytorch-get-started/tree/master/src/touchtext',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
    ],
    license='MIT License',
    packages=['touchtext'],
    entry_points={
    },
    install_requires=[
        'torch >= 2.3.1',
        'tqdm',
    ],
)
