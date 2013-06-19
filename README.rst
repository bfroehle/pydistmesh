PyDistMesh_: A Simple Mesh Generator in Python
==============================================

PyDistMesh_ is a simple Python code for generating unstructured
triangular and tetrahedral meshes using *signed distance functions*. It
intends to have the same functionality as and similar interface to the
MATLAB-based DistMesh_. Like DistMesh, upon which it is based,
PyDistMesh is distributed under the `GNU GPL`_.

.. _PyDistMesh: https://github.com/bfroehle/pydistmesh
.. _DistMesh: http://persson.berkeley.edu/distmesh/
.. _`GNU GPL`: http://www.gnu.org/copyleft/gpl.html

2-D Examples
------------

* Uniform Mesh on Unit Circle::

     >>> import distmesh as dm
     >>> import numpy as np
     >>> fd = lambda p: np.sqrt((p**2).sum(1))-1.0
     >>> p, t = dm.distmesh2d(fd, dm.huniform, 0.2, (-1,-1,1,1))

* Rectangle with circular hole, refined at circle boundary::

     >>> import distmesh as dm
     >>> fd = lambda p: dm.ddiff(dm.drectangle(p,-1,1,-1,1),
     ...                         dm.dcircle(p,0,0,0.5))
     >>> fh = lambda p: 0.05+0.3*dm.dcircle(p,0,0,0.5)
     >>> p, t = dm.distmesh2d(fd, fh, 0.05, (-1,-1,1,1),
     ...                      [(-1,-1),(-1,1),(1,-1),(1,1)])


3-D Examples
------------

* 3-D Unit ball::

     >>> import distmesh as dm
     >>> import numpy as np
     >>> fd = lambda p: np.sqrt((p**2).sum(1))-1.0
     >>> p, t = dm.distmeshnd(fd, dm.huniform, 0.2, (-1,-1,-1, 1,1,1))

* Cylinder with hole::

     >>> import distmesh as dm
     >>> import numpy as np
     >>> def fd10(p):
     ...     r, z = np.sqrt(p[:,0]**2 + p[:,1]**2), p[:,2]
     ...     d1, d2, d3 = r-1.0, z-1.0, -z-1.0
     ...     d4, d5 = np.sqrt(d1**2+d2**2), np.sqrt(d1**2+d3**2)
     ...     d = dm.dintersect(dm.dintersect(d1, d2), d3)
     ...     ix = (d1>0)*(d2>0); d[ix] = d4[ix]
     ...     ix = (d1>0)*(d3>0); d[ix] = d5[ix]
     ...     return dm.ddiff(d, dm.dsphere(p, 0,0,0, 0.5))
     >>> def fh10(p):
     ...     h1 = 4*np.sqrt((p**2).sum(1))-1.0
     ...     return np.minimum(h1, 2.0)
     >>> p, t = dm.distmeshnd(fd10, fh10, 0.1, (-1,-1,-1, 1,1,1))

Demos
-----

For a quick demonstration, run::

    $ python -m distmesh.demo2d

or::

    $ python -m distmesh.demond

Dependencies
------------

PyDistMesh is compatible with both Python 2 and Python 3. (The author
has only tested it in Python 2.7 and Python 3.2). It requires several
common Python packages:

* NumPy_
* SciPy_
* matplotlib_ (optional)

Building the package requires a C compiler and LAPACK_.  Cython_, if
available, can be used to rebuild the extension module bindings.

.. _NumPy: http://numpy.scipy.org/
.. _SciPy: http://scipy.org/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _Cython: http://cython.org/
.. _LAPACK: http://www.netlib.org/lapack/

References
----------

The DistMesh_ algorithm is described in the following two references.
If you use the algorithm in a program or publication, please
acknowledge its authors by adding a reference to the first paper
below.

* P.-O. Persson, G. Strang, **A Simple Mesh Generator in MATLAB**.
  *SIAM Review*, Volume 46 (2), pp. 329-345, June 2004 (`PDF
  <http://persson.berkeley.edu/distmesh/persson04mesh.pdf>`__)

* P.-O. Persson, **Mesh Generation for Implicit Geometries**.
  Ph.D. thesis, *Department of Mathematics, MIT*, Dec 2004 (`PDF
  <http://persson.berkeley.edu/thesis/persson-thesis-color.pdf>`__)
