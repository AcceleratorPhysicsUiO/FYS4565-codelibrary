#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
beamGeneratorLibrary.py
    Lorem ipsum...
"""

import numpy as np
import matplotlib.pyplot as plt

def generateBeam(N:int,\
                 betaX:float,alphaX:float,epsgX:float,\
                 betaY:float,alphaY:float,epsgY:float,\
                 sigmaE:float, sigmaZ:float,\
                 E0:float, x0:float=0.0,xp0:float=0.0, y0=0.0,yp0=0.0,\
                 rng=np.random.default_rng(42)) -> np.ndarray:
    """
    Generate macro-particles with the given Twiss parameters [m,1,m] in 4D and momentum spread (RMS of relative to total momentum),
    producing an 6xN array of particle phase-space coordinates

    Parameters
    ------------
    N
        Number of macro-particles to generate            [1]
    betaX, alphaX, epsgX
        TWISS parameters for the horizontal plane        [m,1,m]
    betaY, alphaY, epsgY
        TWISS parameters for the vertical   plane        [m,1,m]
    sigmaPP
        Relative energy spread deltaP/P                  [1]
    sigmaZ
        Bunch length sigma                               [m]
    E0
        Average energy of generated particles [eV]
        This is typically equal to the reference energy of the beam
    x0,xp0,y0,yp0
        Initial beam position in phase space (x,x',y,y') [m,1,m,1]
        Defaults to 0.0
    rng
        An initialized random number generator "dice" from ``np.random.Generator``.
        Defaults to ``np.random.default_rng(42)``

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

    """

    covX = epsgX*np.array([[betaX, -alphaX],[-alphaX, (1+alphaX**2)/betaX]])
    covY = epsgY*np.array([[betaY, -alphaY],[-alphaY, (1+alphaY**2)/betaY]])

    partX = rng.multivariate_normal(mean=[x0,xp0], cov=covX, size=N).T
    partY = rng.multivariate_normal(mean=[y0,yp0], cov=covY, size=N).T

    E = rng.normal(loc=E0, scale=sigmaE, size=N)
    
    z = rng.normal(loc=0, scale=sigmaZ, size=N)

    return np.vstack((partX, partY, z, E))


if __name__ == "__main__":
    print ("Hello")
