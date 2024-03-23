#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Util.py
    Library for collecting various useful functions and physics constants
    in the Python library for FYS4565 UiO Particle accelerators course.
    
    Version of 23/01/2024
    
    Created by K. Sjobak.
"""

import numpy as np

#Physics constants:
#: Electron charge [C]
SI_e = 1.60217662e-19
#: Speed of light [m/s]
SI_c = 299792458
#: Proton mass [eV/c^2]
m0_proton = 938.27e6
#: Electron mass [eV/c^2]
m0_electron = 510.998950000e3

#Pretty-printing function
def printMatrixAll(M : np.ndarray, rowLabels : bool = True, colLabels : bool = True) -> None:
    """
    Pretty-printing a numpy 2D matrix

    Parameters
    -----------
    M : np.ndarray with 2D matrix
        The matrix to pretty-print
    Returns
    -------
    None : None
        Nothing is returned
    
    Other parameters
    ----------------
    rowLabels : bool
        Should the rows be labeled in the output?
        Default is True.
    colLabels: bool
        Should the cols be labeled in the output?
        Default is True.
    """
    print(printMatrixAll_str(M,rowLabels,colLabels))

def printMatrixAll_str(M : np.ndarray, rowLabels:bool=True, colLabels:bool=True) -> str:
    """
    Same as `prettyPrintMatrixAll()`, but returns a str (with multiple lines) instead of directly printing it.
    The string is not termiated with a newline.
    """
    ret = ''
    if colLabels:
        ret += " [i,j] | "
        ret += f'     j = 0 '
        for i in range(1,M.shape[1]):
            ret += f'{i:10} '
        ret += '\n'
        ret += "-------|-"+"-"*(10+1)*M.shape[1]+'\n'

    for i in range(M.shape[0]):
        if rowLabels:
            if i > 0:
                ret += f"{i:6} | "
            else:
                ret += f" i = 0 | "
        for j in range(M.shape[1]):
            ret += f'{M[i,j]:10.3e} '
        if i < M.shape[0]-1:
            ret += '\n'
    return ret