#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ObligUtil.py
    Library for collecting various useful functions and physics constants
    for the 2024 project in FYS4565 UiO / Particle accelerators course.
    
    Version of 31/03/2024
    
    Created by K. Sjobak.
"""

import numpy as np
import matplotlib.pyplot as plt

#Import packages from the FYS4565 code library
# Note: the code library must be in a subfolder of this folder, OR in $PYTHONPATH
import FYS4565_codelibrary.Util
import FYS4565_codelibrary.BeamlineElements

#Import functions from the library

### Task 1.1 ###

driftMatrix2D     = FYS4565_codelibrary.BeamlineElements.MakeElemMatrix2D_Drift
quadMatrix2D_thin = FYS4565_codelibrary.BeamlineElements.MakeElemMatrix2D_QuadThin

### Task 1.2 ###

def driftList2D(L,ds):
    N_approx = L/ds
    N = int(np.ceil(N_approx))
    dL = L/float(N)

    Mlist = []
    dslist = []

    for i in range(N):
        Mlist.append(driftMatrix2D(dL))
        dslist.append(ds)
    
    return (Mlist,dslist)

def FODOlist2D_thin(f, L, dS=None):
    Mlist = []
    dslist = []

    Mlist.append(quadMatrix2D_thin(2*f))
    dslist.append(0.0)
    
    if dS == None:
        dS = L
    (Mdrifts,sdrifts) = driftList2D(L,dS)
    Mlist += Mdrifts
    dslist += sdrifts

    Mlist.append(quadMatrix2D_thin(-f))
    dslist.append(0)

    (Mdrifts,sdrifts) = driftList2D(L,dS)
    Mlist += Mdrifts
    dslist += sdrifts

    Mlist.append(quadMatrix2D_thin(2*f))
    dslist.append(0)

    return (Mlist, dslist)

def getBMatrix(alpha,beta):
    B = [[beta, -alpha],[-alpha, (1+alpha**2)/beta]]
    return np.asarray(B)

def getTwiss(B):
    beta = B[0,0]
    alpha = -B[0,1]

    return (alpha, beta)

def evolveB(M,B0):
    B = M @ B0 @ M.T
    return B

def evolveBList(Mlist, B0):
    B = B0
    Blist = []
    for M in Mlist:
        B = evolveB(M,B)
        Blist.append(B)
    return Blist

def plotTwissFunctions(B0, Mlist, dsList, xy=None, marker=True):
    """
    Given an initial beam matrix B0 and a list of elements
    described by their transfer matrices `Mlist` and thicknesses `dsList`,
    evolve the beta- and alpha functions element-by-element and plot.
    
    The `xy` and `marker` arguments are used to control the plot ylabels.
    
    The axis used for the plot is returned.
    """
    
    if len(Mlist) != len(dsList):
        raise ValueError(f"Got different length for 'elems' ({len(elems)}) and 'dsList' ({len(dsList)})")
    
    #Evolve Twiss functions
    B_sequence  = [B0]
    B_sequence += evolveBList(Mlist,B0)

    s_sequence = [0.0,]
    s = 0.0
    #Cumulative sum of element lengths
    for ds in dsList:
        s += ds
        s_sequence.append(s)

    #Extract the alpha and beta functions    
    
    beta_sequence = []
    alpha_sequence = []
    for B in B_sequence:
        (alpha,beta) = getTwiss(B)
        beta_sequence.append(beta)
        alpha_sequence.append(alpha)
    
    #Interpret plotting directive arguments
    if not xy is None:
        xy = r"_{"+xy+r"}"
    else:
        xy = ""
        
    if marker:
        markerBeta = 'o'
        markerAlpha= '+'
    else:
        markerBeta = None
        markerAlpha = None
    
    #Plot!
    plt.figure()
    
    plt.plot(s_sequence, beta_sequence,'b-', marker=markerBeta)
    plt.ylabel(r'$\beta' + xy + r'$')
    plt.xlabel('s [m]')
    ax1=plt.gca()
    ax1.yaxis.label.set_color('blue')
    ax1.spines['left'].set_color('blue')
    ax1.tick_params(axis='y',color='blue')
    
    ax2=plt.twinx()
    plt.plot(s_sequence, alpha_sequence, 'r-', marker=markerAlpha)
    plt.ylabel(r'$\alpha' + xy + r'$')
    ax2.yaxis.label.set_color('red')
    ax2.spines['left'].set_color('blue')
    ax2.spines['right'].set_color('red')
    ax2.tick_params(axis='y',color='red')
    
    return(ax1,ax2)

### Task 1.3 ###

def matchingSectionList2D_thin(f1,f2,fFODO=38.0, dS=None):
    Mlist = []
    dslist = []

    L1 = 50.0           #[m] To first quad
    L2 = 75.0-L1        #[m] To second quad
    L3 = 95-(L2+L1)     #[m] To diagnostics screen
    L4 = 100-(L3+L2+L1) #[m] To end

    if dS == None:
        dS1 = L1
    else:
        dS1 = dS
    (Mdrifts,sdrifts) = driftList2D(L1,dS1)
    Mlist += Mdrifts
    dslist += sdrifts

    Mlist.append(quadMatrix2D_thin(f1))
    dslist.append(0.0)
    
    if dS == None:
        dS2 = L2
    else:
        dS2 = dS
    (Mdrifts,sdrifts) = driftList2D(L2,dS2)
    Mlist += Mdrifts
    dslist += sdrifts

    Mlist.append(quadMatrix2D_thin(-f2))
    dslist.append(0.0)

    if dS == None:
        dS = L3
    (Mdrifts,sdrifts) = driftList2D(L3,dS)
    Mlist += Mdrifts
    dslist += sdrifts

    if dS == None:
        dS = L3
    (Mdrifts,sdrifts) = driftList2D(L4,dS)
    Mlist += Mdrifts
    dslist += sdrifts

    Mlist.append(quadMatrix2D_thin(fFODO*2))
    dslist.append(0.0)

    return (Mlist, dslist)
