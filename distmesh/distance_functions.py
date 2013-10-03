# encoding: utf-8
"""Distance functions."""

#-----------------------------------------------------------------------------
#  Copyright (C) 2004-2012 Per-Olof Persson
#  Copyright (C) 2012 Bradley Froehle

#  Distributed under the terms of the GNU General Public License. You should
#  have received a copy of the license along with this program. If not,
#  see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import numpy as np
import sympy as sp
from sympy.utilities import lambdify

__all__ = [
    # Distance functions:
    'dblock',
    'dcircle',
    'ddiff',
    'dellipse',
    'dellipsoid',
    'dexpr',
    'dintersect',
    'dmatrix3d',
    'dmatrix',
    'dpoly',
    'drectangle',
    'drectangle0',
    'dsegment',
    'dsphere',
    'dunion',

    # Mesh size functions:
    'hmatrix3d',
    'hmatrix',
    'huniform',

    # Generic node manipulation:
    'protate',
    'pshift',
    ]

# These are used very often:
min = np.minimum
max = np.maximum

#-----------------------------------------------------------------------------
# Signed distance functions
#-----------------------------------------------------------------------------

def dblock(p,x1,x2,y1,y2,z1,z2):
    return -min(min(min(min(min(-z1+p[:,2],z2-p[:,2]),-y1+p[:,1]),y2-p[:,1]),-x1+p[:,0]),x2-p[:,0])

def dcircle(p,xc,yc,r):
    """Signed distance to circle centered at xc, yc with radius r."""
    return np.sqrt(((p-np.array([xc,yc]))**2).sum(-1))-r

def ddiff(d1,d2):
    """Signed distance to set difference between two regions described by
    signed distance functions d1 and d2.

    Not exact the true signed distance function for the difference,
    for example around corners.
    """
    return max(d1,-d2)

from distmesh._distance_functions import dellipse

from distmesh._distance_functions import dellipsoid


#-----------------------------------------------------------------------------
# dexpr using sympy
#-----------------------------------------------------------------------------


def dexpr(p, fstr, nit=20, alpha=0.1):
    """
    Returns distance function based on zero level set of function fstr.
    fstr is a string to be evaluated by sympy.sympify. It _must_ use
    x, y as variables in the string.
    """

    x, y = sp.symbols('x y')
    f = sp.sympify(fstr)
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    fxx = lambdify((x, y), sp.diff(fx, x))
    fyy = lambdify((x, y), sp.diff(fy, y))
    fxy = lambdify((x, y), sp.diff(fx, y))
    f = lambdify((x, y), f)
    fx = lambdify((x, y), fx)
    fy = lambdify((x, y), fy)

    x0 = p[:, 0]
    y0 = p[:, 1]
    x = x0
    y = y0

    for it in range(nit):
        cf = f(x, y)
        cfx = fx(x, y)
        cfy = fy(x, y)
        cfxx = fxx(x, y)
        cfyy = fyy(x, y)
        cfxy = fxy(x, y)

        F1 = cf
        F2 = (x - x0) * cfy - (y - y0) * cfx
        J11 = cfx
        J12 = cfy
        J21 = cfy + (x - x0) * cfxy - (y - y0) * cfxx
        J22 = -cfx - (y - y0) * cfxy + (x - x0) * cfyy

        detJ = J11 * J22 - J12 * J21
        detJ[detJ == 0] = np.inf

        x = x - alpha * (J22 * F1 - J21 * F2) / detJ
        y = y - alpha * (-J12 * F1 + J11 * F2) / detJ

    return np.sqrt((x - x0) ** 2 + (y - y0) ** 2) * np.sign(f(x0, y0))


def dintersect(d1,d2):
    """Signed distance to set intersection of two regions described by signed
    distance functions d1 and d2.

    Not exact the true signed distance function for the difference,
    for example around corners.
    """
    return max(d1,d2)

def dmatrix3d(p,xx,yy,zz,dd):
    """Signed distance function by interpolation of the values dd on the
    Cartesian grid xx, yy, zz."""
    return ml.interp3_linear(xx,yy,zz,dd,p[:,0],p[:,1],p[:,2])

def dmatrix(p,xx,yy,dd):
    """Signed distance function by interpolation of the values dd on the
    Cartesian grid xx, yy."""
    return ml.interp2_linear(xx,yy,dd,p[:,0],p[:,1])

def dpoly(p,pv):
    """Signed distance function for polygon with vertices pv.

    Usually pv should also be provided as fixed points in distmesh2d.

    pv should be provided as a list of coordinates [(x0,y0), (x1,y1), ...]
    or an array of shape (nv, 2).
    """
    from matplotlib.nxutils import points_inside_poly
    return (-1)**points_inside_poly(p, pv) * dsegment(p, pv).min(1)

def drectangle0(p,x1,x2,y1,y2):
    """Signed distance function for rectangle with corners (x1,y1), (x2,y1),
    (x1,y2), (x2,y2).

    See drectangle for a simpler version ignoring corners.
    """
    d1=y1-p[:,1]
    d2=-y2+p[:,1]
    d3=x1-p[:,0]
    d4=-x2+p[:,0]

    d5=np.sqrt(d1**2+d3**2)
    d6=np.sqrt(d1**2+d4**2)
    d7=np.sqrt(d2**2+d3**2)
    d8=np.sqrt(d2**2+d4**2)

    d=-min(min(min(-d1,-d2),-d3),-d4)

    ix=(d1>0)*(d3>0)
    d[ix]=d5[ix]
    ix=(d1>0)*(d4>0)
    d[ix]=d6[ix]
    ix=(d2>0)*(d3>0)
    d[ix]=d7[ix]
    ix=(d2>0)*(d4>0)
    d[ix]=d8[ix]

    return d

def drectangle(p,x1,x2,y1,y2):
    """Signed distance function for rectangle with corners (x1,y1), (x2,y1),
    (x1,y2), (x2,y2).

    This has an incorrect distance to the four corners. See drectangle0 for a
    true distance function.
    """
    return -min(min(min(-y1+p[:,1],y2-p[:,1]),-x1+p[:,0]),x2-p[:,0])

from distmesh._distance_functions import dsegment

def dsphere(p,xc,yc,zc,r):
    """Signed distance function for a sphere centered at xc,yc,zc with radius
    r."""
    return np.sqrt((p[:,0]-xc)**2+(p[:,1]-yc)**2+(p[:,2]-zc)**2)-r

def dunion(d1,d2):
    """Signed stance function for the set union of two regions described by
    signed distance functions d1, d2.

    This not a true signed distance function for the union, for example around
    corners.
    """
    return min(d1,d2)

#-----------------------------------------------------------------------------
# Mesh size functions
#-----------------------------------------------------------------------------

def hmatrix3d(p,xx,yy,zz,dd,hh):
    """Mesh size function by interpolation of the values hh on the Cartesian
    grid xx, yy, zz."""
    return ml.interp3_linear(xx,yy,zz,hh,p[:,0],p[:,1],p[:,2]);

def hmatrix(p,xx,yy,dd,hh):
    """Mesh size function by interpolation of the values hh on the Cartesian
    grid xx, yy."""
    return ml.interp2_linear(xx,yy,hh,p[:,1],p[:,2]);

def huniform(p):
    """Implements the trivial uniform mesh size function h=1."""
    return np.ones(p.shape[0])

#-----------------------------------------------------------------------------
# Generic node manipulation
#-----------------------------------------------------------------------------

def protate(p,phi):
    """Rotate points p the angle phi around origin."""
    A = np.array(((np.cos(phi), -np.sin(phi)),
                  (np.sin(phi),  np.cos(phi))))
    return p.dot(A)

def pshift(p,x0,y0):
    """Move points p by (x0,y0)."""
    return p + [x0,y0]
