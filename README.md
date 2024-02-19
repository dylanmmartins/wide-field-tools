# Wide-field tools

Preprocessing tools for one-photon wide-field microscopy data.

## Installation

Create the conda environment from the `environment.yml` file:

```conda env create -f environment.yml```

and install this repository as the package `wfTools1` with

```pip install -e .```

## Functions

**Load and register image stack**

Read a multi-page tif file from the file path, and return a numpy array. The flag `rotate` can be used to rotate the image 180 degrees (`default=True`). The flag `ds` downsamples the image in the x and y dimensions by the factor `ds` (e.g., a value of 0.25 reduces the image to 25% of its original size; `default=0.25`). The flag `doReg` runs an image stack registration subroutine to align the images in the stack before it is returned as an array (`default=True`).

Before running this function, make sure that the tif stack is a single multi-page tif file. If the tif stack is a folder of individual tif files, use the MATLAB subroutine, `subroutine_tifConvert.m` to convert the folder of tif files into a single multi-page tif file, and then pass that path into this function. (see [this](https://github.com/ucsb-goard-lab/Two-photon-calcium-post-processing/blob/main/subroutine/subroutine_tifConvert.m) MATLAB code).

```
import wfTools as wft

path = 'path/to/tif/stack.tif'
img = wft.load_tif_stack(path, rotate=True, ds=0.25, doReg=True)
```