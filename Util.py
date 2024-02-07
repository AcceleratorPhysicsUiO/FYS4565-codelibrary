#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Util.py
    Library for collecting various useful functions and constants
    in the Python library for FYS4565 UiO Particle accelerators course.
    
    Version of 23/01/2024
    
    Created by K. Sjobak.
"""

import numpy as np

#Physics constants:
SI_e = 1.60217662e-19 #[C]
SI_c = 299792458      #[m/s]

m0_proton = 938.27e6  #[eV/c^2]

#Pretty-printing function
def printMatrixAll(M : np.ndarray, rowLabels=True, colLabels=True) -> None:
    "Pretty printing a numpy 2D matrix M"
    print(printMatrixAll_str(M,rowLabels,colLabels))

def printMatrixAll_str(M : np.ndarray, rowLabels=True, colLabels=True) -> str:
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