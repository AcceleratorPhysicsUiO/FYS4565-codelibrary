#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParticleBeamManager.py
    Library for generating beam distributions by Monte Carlo sampling,
    and for saving/loading them to .csv (text) files.
    
    Version of 23/01/2024
    
    Created by K. Sjobak.
"""

import numpy as np

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
    quiet : boolean
        If False, some diagnostics output is printed during operation.
        If True, this is suppressed.
        Defaults to False

    Examples
    --------
    A simple example, specifying number of particles, average energy,
    Twiss parameters, and some other extra named parameters::

        import ParticleBeamManager
        B_gen = ParticleBeamManager.generateBeam(10000, 10.0e9, \
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

def saveBeamFile_csv(beamFileName, partArray, quiet=False):
    """
    Saves the content of a beam array to a CSV file.
    
    Parameters
    ----------
    beamFileName : string
        Filename (ending in .csv or .CSV) to save the array to
    partArray : np.ndarray
        6xN array of particles

    Returns
    -------
    Nothing is returned from this method

    Other parameters
    ----------------
    quiet : boolean
    If False, some diagnostics output is printed during operation.
        If True, this is suppressed.
        Defaults to False
    
    Examples
    --------

    >>> ParticleBeamManager.saveBeamFile_csv('testFile.csv',B_gen)

    """
    if not (beamFileName.endswith('.csv') or beamFileName.endswith('.CSV')):
        raise ValueError('BeamFileName should end with .csv or .CSV')
    if not (type(partArray)==np.ndarray and partArray.ndim == 2):
        raise TypeError(f'Expected partArray to be a numpy.ndarray object, got {type(partArray)}')
    if partArray.shape[0] != 6:
        raise TypeError(f'partArray should be a 6xN matrix, but the number of rows was {partArray.shape[0]}')

    if not quiet:
        print(f"Saving N={partArray.shape[1]} to file '{beamFileName}'...")

    np.savetxt(fname=beamFileName, X=partArray.T, fmt='%25.18e', delimiter=', ', header='x[m], xp[1], y[m], yp[1], dZ[m], Ek[eV]')

    if not quiet:
        print('... done!')

def loadBeamFile_csv(beamFileName, quiet=False):
    """
    Loads and returns a beam array from a CSV file

    Parameters
    ----------
    beamFileName : string
        Filename (ending in .csv or .CSV) to load the array from
    
    Returns
    -------
    Returns a 6xN matrix of particles in the same way as from the `generateBeam()` method

    Other parameters
    ----------------
    quiet : boolean
    If False, some diagnostics output is printed during operation.
        If True, this is suppressed.
        Defaults to False
        
    Examples
    --------

    >>> B_load = ParticleBeamManager.loadBeamFile_csv('testFile.csv')

    """
    if not (beamFileName.endswith('.csv') or beamFileName.endswith('.CSV')):
        raise ValueError('BeamFileName should end with .csv or .CSV')
    
    if not quiet:
        print(f"Loading particles from file '{beamFileName}'...")
    
    partArray = np.loadtxt(fname=beamFileName, delimiter=',')
    partArray = partArray.T

    if not quiet:
        print(f"... Done! Loaded N={partArray.shape[1]} particles.")

    return partArray

if __name__ == "__main__":

    #Test the code
    B_gen = generateBeam(10000, 10.0e9, 173.2,0.0,8.58e-08 ,173.2,1.0,8.58e-08, sigmaEk=1e7, sigmaZ=5e-5)
    saveBeamFile_csv('testFile.csv',B_gen)
    B_gen_load = loadBeamFile_csv('testFile.csv')

    #Should be all zeros, or almost
    print(B_gen - B_gen_load)
