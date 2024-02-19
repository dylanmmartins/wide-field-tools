"""
corr.py
Correlation functions.

Author        : Dylan Martins
Written       : Oct 22 2023
Last modified : Dec 03 2023
"""


import numpy as np



def corr1(A, B):
    """Calculate rank correlation coefficient.

    Equivilent to MATLAB's `corr` function. Faster than
    using `np.corrcoef`.

    Parameters
    ----------
    A : array-like
        First array.
    B : array-like
        Second array, with shape same as `A`.

    Returns
    -------
    r : float
        Pearson correlation coefficient.

    """

    A = (A - np.nanmean(A, axis=0)) / A.std(axis=0)
    B = (B - np.nanmean(B, axis=0)) / B.std(axis=0)

    r = (np.dot(B.T, A)/B.shape[0])

    return r

