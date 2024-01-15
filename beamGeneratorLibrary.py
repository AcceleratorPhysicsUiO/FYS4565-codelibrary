#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
beamGeneratorLibrary.py
    Library for generating beam distributions, and for saving/loading them to .csv (text) files.
    Created by K. Sjobak.
"""

import numpy as np
import matplotlib.pyplot as plt

def generateBeam(N:int, Ek0:float,\
                 betaX:float,alphaX:float,epsgX:float,\
                 betaY:float,alphaY:float,epsgY:float,\
                 sigmaEk:float, sigmaZ:float,\
                 x0:float=0.0,xp0:float=0.0, y0=0.0,yp0=0.0,\
                 rng=np.random.default_rng(42), quiet=False) -> np.ndarray:
    """
    Generate macro-particles with the given Twiss parameters [m,1,m] in 4D and momentum spread (RMS of relative to total momentum),
    producing an 6xN array of particle phase-space coordinates

    Parameters
    ------------
    N : integer
        Number of macro-particles to generate            [1]
    Ek0 : float
        Average energy of generated particles [eV]
        This is typically equal to the reference energy of the beam

    betaX, alphaX, epsgX : float
        TWISS parameters for the horizontal plane        [m,1,m]
    betaY, alphaY, epsgY : float
        TWISS parameters for the vertical   plane        [m,1,m]
    
    Returns
    --------
    particleArray : np.ndarray with 6 rows and N columns.
        Array of macro particles, arranged as::

            [[x0  , x1  , x2  , ..., xN  ],
             [xp0 , xp1 , xp2 , ..., xpN ],
             [y0  , y1  , y2  , ..., yN  ],
             [yp0 , yp1 , yp2 , ..., ypN ],
             [z0  , z1  , z2  , ..., zN  ],
             [E0  , E1  , E2  , ..., EN  ]]

        Here the numerical index is the particle index.
    
    Other parameters
    ----------------
    sigmaEk : float
        Relative kinetic energy                          [eV]
        Defaults to 0.0
    sigmaZ : float
        Bunch length sigma                               [m]
        Defaults to 0.0
    x0,xp0,y0,yp0 : float
        Initial beam position in phase space (x,x',y,y') [m,1,m,1]
        Defaults to 0.0
    rng : Subclass of ``np.random.Generator``
        An initialized random number generator "dice" from ``np.random.Generator``.
        Defaults to ``np.random.default_rng(42)``
    quiet : Boolean
        If False, some diagnostics output is printed during operation.
        If True, this is suppressed.
        Defaults to False

    Examples
    --------

    >>> import beamGeneratorLibrary
    >>> B_gen = beamGeneratorLibrary.generateBeam(10000, 10.0e9, \
                                                  173.2, 0.0, 8.58e-08, \
                                                  173.2, 1.0, 8.58e-08, \
                                                  sigmaEk=1e7, sigmaZ=5e-5, \
                                                  rng=np.random.default_rng())

    """

    if not quiet:
        print (f"Generating N={N} macroparticles with Ek0={Ek0:e} [eV]")
        print (f" betaX = {betaX} [m], alphaX = {alphaX}, epsgX = {epsgX:e} [m]")
        print (f" betaY = {betaY} [m], alphaX = {alphaY}, epsgX = {epsgY:e} [m]")
        print (f" sigmaEk = {sigmaEk:e} [eV], sigmaZ={sigmaZ:e} [m]")
        print (f" x0 = {x0:e} [m], xp0 = {xp0:e} [rad], y0 = {y0:e} [m], yp0 = {yp0:e} [rad]")

    covX = epsgX*np.array([[betaX, -alphaX],[-alphaX, (1+alphaX**2)/betaX]])
    covY = epsgY*np.array([[betaY, -alphaY],[-alphaY, (1+alphaY**2)/betaY]])

    partX = rng.multivariate_normal(mean=[x0,xp0], cov=covX, size=N).T
    partY = rng.multivariate_normal(mean=[y0,yp0], cov=covY, size=N).T

    Ek = rng.normal(loc=Ek0, scale=sigmaEk, size=N)
    
    z = rng.normal(loc=0, scale=sigmaZ, size=N)

    if not quiet:
        print("Done!")
    return np.vstack((partX, partY, z, Ek))

def saveBeamFile_csv(beamFileName, partArray):
    """
    Saves the content of a beam array to a CSV file.
    """
    np.savetxt(fname=beamFileName, X=partArray.T, fmt='%25.18e', delimiter=', ', header='x[m], xp[1], y[m], yp[1], dZ[m], Ek[eV]')

def loadBeamFile_csv(beamFileName):
    """
    Loads and returns a beam array from a CSV file

    """
    partArray = np.loadtxt(fname=beamFileName, delimiter=',')
    partArray = partArray.T
    return partArray

if __name__ == "__main__":

    #Test the code
    B_gen = generateBeam(10000, 10.0e9, 173.2,0.0,8.58e-08 ,173.2,1.0,8.58e-08, sigmaEk=1e7, sigmaZ=5e-5)
    saveBeamFile_csv('testFile.csv',B_gen)
    B_gen_load = loadBeamFile_csv('testFile.csv')

    #Should be all zeros, or almost
    print(B_gen - B_gen_load)
