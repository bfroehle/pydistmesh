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
import numpy as np
from numpy.distutils import system_info

from distutils.core import setup
from distutils.extension import Extension


# Read version from distmesh/__init__.py
with open(os.path.join('distmesh', '__init__.py')) as f:
    line = f.readline()
    while not line.startswith('__version__'):
        line = f.readline()
exec(line, globals())


# Build list of cython extensions
ext_modules = [
    Extension(
        'distmesh._distance_functions',
        sources=[os.path.join('distmesh', '_distance_functions.c')],
        depends=[os.path.join('distmesh', 'src', 'distance_functions.c')],
        include_dirs=[np.get_include()],
    ),
]

# distmesh._distance_functions needs LAPACK
lapack_info = system_info.get_info('lapack_opt', 0)
# See ('https://github.com/nipy/nipy/blob/'
#      '91fddffbae25a5ca3a5b35db2a7c605b8db9014d/nipy/labs/setup.py#L44')
if 'libraries' not in lapack_info:
    lapack_info = system_info.get_info('lapack', 0)

ext_modules[0].libraries.extend(lapack_info['libraries'])
ext_modules[0].library_dirs.extend(lapack_info['library_dirs'])
if 'include_dirs' in lapack_info:
    ext_modules[0].include_dirs.extend(lapack_info['include_dirs'])

install_requires = [
    'matplotlib>=1.2',
]

long_description = open('README.rst').read()

setup(name='PyDistMesh',
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
      install_requires=install_requires,
      license='GPL',
      packages=['distmesh'],
      ext_modules=ext_modules,
)
