#!/usr/bin/env python

# This file is part of Build Your Own Config
#
# Copyright 2018 Vincent Ladeuil
# Copyright 2013-2016 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


import setuptools

import byoc


setuptools.setup(
    name='python3-byoc',
    version='.'.join(str(c) for c in byoc.__version__[0:3]),
    description=('Build Your Own Config framework.'),
    author='Vincent Ladeuil',
    author_email='v.ladeuil+lp@free.fr',
    url='https://launchpad.net/byoc',
    license='GPLv3',
    packages=['byoc', 'byoc.tests'],
)
