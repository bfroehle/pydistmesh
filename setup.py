#!/usr/bin/env python

#-----------------------------------------------------------------------------
#  Copyright (C) 2012 Bradley Froehle

#  Distributed under the terms of the GNU General Public License. You should
#  have received a copy of the license along with this program. If not,
#  see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import os

from distutils.core import setup

# Read version from distmesh/__init__.py
with open(os.path.join('distmesh', '__init__.py')) as f:
    line = f.readline()
    while not line.startswith('__version__'):
        line = f.readline()
exec(line, globals())

# Build list of cython extensions
try:
    from Cython.Build import cythonize
    ext_modules = cythonize([
        os.path.join('distmesh', '_distance_functions.pyx'),
        ])
except ImportError:
    from distutils.extension import Extension
    ext_modules = [
        Extension(
            'distmesh._distance_functions',
            [os.path.join('distmesh', '_distance_functions.c')],
            ),
        ]

# distmesh._distance_functions needs LAPACK
ext_modules[0].libraries.append('lapack')

long_description = open('README.rst').read()

setup(name='distmesh',
      version=__version__,
      description="A Simple Mesh Generator in Python",
      long_description=long_description,
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Operating System :: POSIX :: Linux',
          'Topic :: Scientific/Engineering :: Mathematics',
      ],
      keywords='meshing',
      author='Bradley Froehle',
      author_email='brad.froehle@gmail.com',
      url='https://github.com/bfroehle/pydistmesh',
      license='GPL',
      packages=['distmesh'],
      ext_modules=ext_modules,
)
