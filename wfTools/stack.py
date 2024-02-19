"""
stack.py
Image stack operations.

Author        : Dylan Martins
Written       : Nov 09 2023
Last modified : Jan 26 2024
"""


import numpy as np
from tqdm import tqdm
import tifffile as tiff
import skimage.registration
import scipy.ndimage



def register_stack_to_template(stack):
    """ Register a stack of images to a template image.

    Parameters
    ----------
    stack : np.ndarray
        Image stack as a 3D numpy array.

    Returns
    -------
    stack : np.ndarray
        Image stack with shifted images.
    extras : dict
        Dictionary of extra variables. Variables are
        'x_shift', 'y_shift', and 'shifterr', (the shift
        values and the error for each frame, respectively).

    """

    template = stack[0,:,:].copy()

    # Initialize arrays to store shift values
    x_shift = np.zeros(np.size(stack, axis=0))
    y_shift = np.zeros(np.size(stack, axis=0))
    shifterr = np.zeros(np.size(stack, axis=0))


    print('Starting stack registration')
    for i in tqdm(range(np.size(stack, axis=0))):
        # shift image to match template
        shift, error, _ = skimage.registration.phase_cross_correlation(
            reference_image=template,
            moving_image=stack[i,:,:],
            upsample_factor=4
        )

        x_shift[i] = shift[0]
        y_shift[i] = shift[1]
        shifterr[i] = error

        # Apply shift to image
        stack[i,:,:] = scipy.ndimage.shift(
            stack[i,:,:],
            shift,
            mode='constant',
            cval=np.nan
        )

    # Make a dictionary of extras to return
    extras = {
        'x_shift': x_shift,
        'y_shift': y_shift,
        'shifterr': shifterr
    }

    # Return stack with shifted images
    return stack, extras



def load_tif_stack(path, rotate=True, ds=0.25, doReg=True):
    """ Load a tif stack into a numpy array.

    Before running this function, make sure that the tif stack is a
    single multi-page tif file. If the tif stack is a folder of
    individual tif files, use the MATLAB subroutine, `subroutine_tifConvert.m`
    to convert the folder of tif files into a single multi-page tif file,
    and then pass that path into this function. (see
    https://github.com/ucsb-goard-lab/Two-photon-calcium-post-processing/blob/main/subroutine/subroutine_tifConvert.m
    for the MATLAB code).

    Parameters
    ----------
    path : str
        Path to tif stack, which needs to be a single multi-page
        tif file.
    rotate : bool
        Rotate the image by 180 deg.
    ds : float
        Downsample the image by this factor. If this value is set
        to 1, the image will remaind and full-size. Default is 0.25,
        which resizes to one-quarter of the original size.
    doReg : bool
        Register the image stack to a template. Default is True.

    Returns
    -------
    tif_array : np.ndarray
        Image stack as a numpy array.
    """

    tif_array = tiff.imread(path)

    # Rotate by 180 deg
    if rotate is True:
        for i in range(np.size(tif_array, axis=0)):
            tif_array[i,:,:] = np.flipud(np.fliplr(tif_array[i,:,:]))

    # Downsample, to 1/4 original resolution along axis 1 and 2
    if ds != 1:
        tif_array = tif_array[:, ::int(1/ds), ::int(1/ds)]

    # Image stack registration
    if doReg is True:
        tif_array, _ = register_stack_to_template(tif_array)

    return tif_array

