#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BeamlineSequence.py
    Library for organizing beamline elements into sequences.
    
    Version of 06/02/2024
    
    Created by K. Sjobak.
"""

import numpy as np
import Util

class ElementSequence:
    """
    Organizes a list of beamline elements.
    """

    def __init__(self, elementMatrices : list|None = [], elementLengths : list = None, is2D:bool=True):
        """
        The constructor creates a new ElementSequence containing a list of 2D or 6D element matrices,
        and optionally a list of lengths representing their lengths.

        Parameters
        ----------
        elementMatrices : Python List ([...]) of 2x2 or 6x6 arrays
            List of 2x2 or 6x6 numpy arrays representing the action on the particles for each element
            See `BeamlineElements.py` for information on how to create such elements
            Default is [] (empty list)

        Returns
        -------
        self : ElementSequence
            Returns a new instance of `ElementSequence`.
    
        Other parameters
        ----------------
        elementLengths : Python List ([...]) or None
            The length [m] of each element. If None, elementLenghts is assumed to be unknown in this ElementSequence.
            Default is None.
            Tip: If creating an empty ElementSequence with elementLengths, set this to [].
        
        is2D : bool
            If True, use 2x2 matrices in elementMatrices, otherwise use 6x6
            Default is True
    
        Example
        -------
    
        >>> import BeamLine
        >>> BL = BeamLine.ElementSequence([],[])

        """

        if not type(elementMatrices) == list:
            raise TypeError("Error in initializing ElementSequence: Expected `elementMatrices` to be a Python list `[]` of matrices")
        
        if elementLengths is None:
            self.hasElementLengths = False
        else:
            self.hasElementLengths = True
            if not type(elementLengths) == list:
                raise TypeError("Error in initializing ElementSequence: Expected `elementLengths` to be a Python list `[]` of floats")
            if len(elementMatrices) != len(elementLengths):
                raise ValueError(f"Error in initializing ElementSequence: Expected `elementMatrices` and `elementLengths` to have the same lengths, got {len(elementMatrices)} and {len(elementLengths)}.")
            self.elementLengths = []
        
        if not type(is2D)==bool:
            raise TypeError('Error in initializing ElementSequence: Type of is2D must be bool')
        self.is2D = is2D

        self.elementMatrices = []
        
        #Add all the elements to the list!
        for i in range(len(elementMatrices)):
            if self.hasElementLengths:
                el = elementLengths[i]
            else:
                el = None
            self.appendElement(elementMatrices[i],el)

    
    def appendElement(self, elementMatrix : np.ndarray, elementLength : float|None = None, insertAfterIndex : int|None = None):
        """
        Adds an element described by a matrix to the sequence.
        If the beamline is initialized with element lengths, an element length is required.
        A 2x2 or 6x6 matrix is expected based on the setting of the is2D flag to the constructor.
        Elements can optionally be added to the middle of the sequence.

        Parameters
        ----------

        elementMatrix : np.ndaray with 2x2 or 6x6 elements
            The matrix describing the element to add.

        elementLength : float or int, or None
            The length of the element, or None in case of a sequence without lengths.
            Default is None

        Returns
        -------
        None : None
            Nothing is returned, but the ElementSequence object is modified.
        
        Other parameters
        ----------------

        insertAfterIndex : int or None
            If given, insert the element into the given position.
            Works like list.insert().
            If not given, the element is inserted at the end of the sequence.
        
        Example
        -------

        >>> import BeamLine
        >>> BL = BeamLine.ElementSequence()
        >>> BL.appendElement(np.eye(2))                      #Appends to end of sequence
        >>> BL.appendElement(np.eye(2), insertAfterIndex=0)  #Inserts to beginning of sequence
        >>> BL.appendElement(np.eye(2), insertAfterIndex=-1) #Inserts to second-to-last position



        """
        #Check input
        if not type(elementMatrix) == np.ndarray:
            raise TypeError('Error in appendElement - expected type(elementMatrix) to be np.ndarray')
        if self.is2D:
            if not elementMatrix.shape == (2,2):
                raise ValueError(f"Trying to append a {elementMatrix.shape} element to a 2D sequence, this is not possible.")
        else:
            if not elementMatrix.shape == (6,6):
                raise ValueError(f"Trying to append a {elementMatrix.shape} element to a 6D sequence, this is not possible.")
        
        if self.hasElementLengths:
            if elementLength is None:
                raise ValueError("Error in appendElement - expected length, got None")
            if not (type(elementLength) == float or type(elementLength) == int):
                raise ValueError("Error in appendElement - expected length to be float or int")

        #Interpret insertAfterIndex
        if insertAfterIndex == None:
            insertAfterIndex = len(self.elementMatrices)

        #Append the element!
        self.elementMatrices.insert(insertAfterIndex, elementMatrix.copy()) #Note: a.copy() will default to making a C-order array.
        if self.hasElementLengths:
            self.elementLengths.insert(insertAfterIndex, elementLength)

    def getPositions(self):
        """
        Get the s positions after every element, or if no element lengths are used, get a position number (int) starting from 0.

        Returns
        -------
        s : np.ndarray
            A 1D numpy array of ints or floats with either element indices or s position of exit.

        """
        if self.hasElementLengths:
            ret = np.array(self.elementLengths,copy=True)
            ret = ret.cumsum()
            return ret
        else:
            ret = np.arange(0,len(self.elementMatrices),1,dtype=int)
            return ret

    def concatenate(self, nextSequence : 'ElementSequence'):
        raise NotImplementedError('TODO')

    def __str__(self):
        """
        Outputs the information in the ElementSequence as a multi-line string.
        
        Returns
        --------
        ret : str
            A string with the information

        Example
        --------

        >>> import BeamLine
        >>> BL = BeamLine.ElementSequence([],[])
        >>> BL.appendElement(np.eye(2),0)
        >>> print(BL)
        ElementSequence:
         - is2D = True
         - hasElementLengths = True
         BeamLineElements contained within:
         Elem #0/1:
         L = 0
         1.000e+00  0.000e+00 
         0.000e+00  1.000e+00 

        """
        ret  = f'ElementSequence:\n'
        ret += f' - is2D = {self.is2D}\n'
        ret += f' - hasElementLengths = {self.hasElementLengths}\n'
        ret += f' BeamLineElements contained within:\n'
        for i in range(len(self.elementMatrices)):
            ret += f' Elem #{i}/{len(self.elementMatrices)}:\n'
            if self.hasElementLengths:
                ret += f' L = {self.elementLengths[i]}\n'
            ret += Util.printMatrixAll_str(self.elementMatrices[i], False,False)
            if i < len(self.elementMatrices)-1:
                ret += '\n'
        if len(self.elementMatrices) == 0:
            ret += " (NO ELEMENTS)\n"
        return ret

if __name__ == '__main__':
    #Some simple self tests

    BL = ElementSequence([],[])
    print(BL)

    import BeamlineElements

    MD = BeamlineElements.MakeElemMatrix2D_Drift(2.0)
    MQf = BeamlineElements.MakeElemMatrix2D_QuadThin(2)
    MQd = BeamlineElements.MakeElemMatrix2D_QuadThin(-2)

    BL.appendElement(np.eye(2),0)

    print(BL)

    BL.appendElement(MQf, 0)
    BL.appendElement(MD, 2.0)
    BL.appendElement(MQd, 0)
    BL.appendElement(MD, 2)

    print (BL)
    print (BL.getPositions())

    BL.appendElement(np.eye(2)*2,0, insertAfterIndex=0)
    print (BL)
    BL.appendElement(np.eye(2)*0,0,insertAfterIndex=-1)
    print (BL)

    print()
    BL2 = ElementSequence([BeamlineElements.MakeElemMatrix6D_Drift(3)],is2D=False)
    
    print (BL2)
    print (BL.getPositions())
