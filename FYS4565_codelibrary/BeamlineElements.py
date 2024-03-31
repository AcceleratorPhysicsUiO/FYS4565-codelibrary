#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BeamlineElements.py
    Library for generating matrices
    representing beamline elements such as magnets and drifts.
    
    Coordinate convention is the same as used for `ParticleBeamManager`, i.e.
    {x,x'} in [m,1] for 2D, or
    {x,x',y,y', z,Ek} in [m, 1, m, 1, m, eV] for 6D

    Version of 31/03/2024
    
    Created by K. Sjobak.
"""

import numpy as np

def MakeElemMatrix2D_QuadThin(f:float) -> np.ndarray:
    """
    Creates a 2x2 matrix representing a quadrupole magnet in the "thin lens" approximation
    in a single plane, given the focal length.
    As a special case for f=0, return an 2x2 identity matrix.

    Parameters
    -----------
    f : float
        Focal length of the magnet [m]

    Returns
    --------
    M : np.ndarray with 2 rows and 2 columns
        A 2x2 matrix representing a 2D thin quadrupole

    Examples
    ---------
    
    >>> import BeamlineElements
    >>> M = BeamlineElements.MakeElemMatrix2D_QuadThin(1.0)

    """

    if f == 0:
        return np.eye(2)

    return np.asarray([ [ 1.0  , 0.0],\
                        [-1.0/f, 1.0] ])

def MakeElemMatrix2D_Drift(L:float) -> np.ndarray:
    """
    Creates a 2x2 matrix representing a drift in a single plane, given its length.

    Parameters
    ----------
    L : float
        Length of the drift section [m]

    Returns
    --------
    M : np.ndarray with 2 rows and 2 columns
        A 2x2 matrix representing a 2D drift

    Examples
    ---------
    
    >>> import BeamlineElements
    >>> M = BeamlineElements.MakeElemMatrix2D_Drift(2.0)

    """
    return np.asarray([ [ 1.0, L  ],\
                        [ 0.0, 1.0] ])

def MakeElemMatrix6D_Drift(L:float) -> np.ndarray:
    """
    Creates a 6x6 matrix representing a drift, given its length.
    Note: The z position is not updated according to the energy offset, but kept unchanged.

    Parameters
    -----------
    L : float
        Length of the drift section

    Returns
    --------
    M : np.ndarray with 6 rows and 6 columns
        A 2x2 matrix representing a 6D drift

    Examples
    ---------
    
    >>> import BeamlineElements
    >>> M = BeamlineElements.MakeElemMatrix6D_Drift(2.0)

    """
    M1 = np.hstack([MakeElemMatrix2D_Drift(L), np.zeros((2,4))])
    M2 = np.hstack([np.zeros((2,2)), MakeElemMatrix2D_Drift(L), np.zeros((2,2))])
    M3 = np.hstack([np.zeros((2,4)), np.eye(2)])
    return np.vstack([M1,M2,M3])

## PUT YOUR OWN ELEMENTS IN BELOW HERE! ##

## ...

## PUT YOUR OWN ELEMENTS ABOVE HERE! ##

if __name__ == "__main__":
    #Self test

    L = 2.0
    f = 1.0

    import Util

    M1 = MakeElemMatrix2D_QuadThin(f)
    Util.printMatrixAll(M1)
    print()

    M2 = MakeElemMatrix2D_Drift(L)
    Util.printMatrixAll(M2)
    print()

    M3 = MakeElemMatrix6D_Drift(L)
    Util.printMatrixAll(M3)
