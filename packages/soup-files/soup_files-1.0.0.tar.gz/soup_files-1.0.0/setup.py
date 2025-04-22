#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
	from setuptools import setup
except Exception as e:
	print(e)
	sys.exit(1)

file_setup = os.path.abspath(os.path.realpath(__file__))
dir_of_project = os.path.dirname(file_setup)

sys.path.insert(0, dir_of_project)

__version__ = '1.0.0'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

setup(
	name='file_paths',
	version=__version__,
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	author_email='brunodasill@gmail.com',
	license='MIT',
	zip_safe=False,
	py_modules=['file_paths'],  # <-- Aqui é o nome do arquivo .py sem a extensão
)


