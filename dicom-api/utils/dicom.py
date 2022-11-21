from pydicom.filereader import dcmread
from pathlib import Path
import numpy as np
import os

def getAllData(files=None, path=None):
    slices = []
    if (files is None):
        directory = Path(os.environ.get("BASE_PATH") + path)
        dicom_list = list(directory.glob('*.dcm'))
        for dicom in dicom_list:
            slices.append(read(dicom))
    else:
        for file in files:
            slices.append(read(file.file))

    slices = calcSliceLocFromPos(slices)
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    return slices

def read(slice):
    return dcmread(slice)

def to3dArray(slices):

    # create a new array of zeros with the same dimensions as the first slice
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # add the 3d image data to new array
    for i, s in enumerate(slices):
        
        slope = s.RescaleSlope
        intercept = s.RescaleIntercept

        pixel_array = s.pixel_array
        
        # Transform to Hounsfield Units
        """ pixel_array = np.float64(pixel_array)
        pixel_array *= slope
        pixel_array += intercept
        pixel_array = np.int16(pixel_array)
        pixel_array = np.clip(pixel_array, -1024, 3071) """

        img2d = pixel_array
        img3d[:, :, i] = img2d

    img3d = np.swapaxes(img3d, 1, 0)
    img3d = np.transpose(img3d)

    return img3d

def calcSliceLocFromPos(slices):
    v = np.subtract(slices[1].ImagePositionPatient, slices[0].ImagePositionPatient)
    v = v / np.linalg.norm(v)
    a = slices[0].ImagePositionPatient
    slices[0].SliceLocation = 0

    for i, slice in enumerate(slices):
        if i > 0:

            p = slice.ImagePositionPatient
            ap = np.subtract(p, a)
            dot = np.dot(ap, v)
            slice.SliceLocation = dot

    return slices