from tomopy.prep.normalize import normalize
import tomopy
import dxchange
import numpy as np
from logger import LOGGER
import os
import tomopy.util.mproc as mproc
import tomopy.util.dtype as dtype
import numexpr as ne
import cv2 as cv


# TODO, REWRITE MORE COMPACT THE TWO RECONSTRUCTION FUNCTIONS


def reconstruct(tomos_3d, flats_3d, darks_3d, sample_name, algorithm="gridrec"):
    tomos = normalize(tomos_3d, flats_3d, darks_3d, cutoff=1.0)
    tomos[np.isnan(tomos)] = 0
    tomos[tomos == -np.inf] = 0
    tomos[tomos == np.inf] = 1
    data = tomopy.minus_log(tomos)
   # data = np.nan_to_num(data)
    theta = tomopy.angles(data.shape[0], 0, 360)

    rot_center = (data.shape[2]) / 2.0
    LOGGER.info(f"Center of rotation image: {rot_center}")

    fname_out_tiff = get_last_folder(sample_name)
    normal_path = os.path.join(fname_out_tiff, "normalized_tomopy")
    os.makedirs(normal_path, exist_ok=True)

    LOGGER.debug("Starting saving normals")
    for i, tomo in enumerate(tomos):
        cv.imwrite(f'{normal_path}/normal_{i}.tiff', tomo)
        LOGGER.debug(f"Saved Normal in {normal_path}/normal_{i}.tiff'")







    slice_start = 0
    slice_end = len(data[0])



    '''
    algorithms = ['art', 'bart', 'fbp', 'gridrec', 'mlem', 'osem',
                  'ospml_hybrid', 'ospml_quad', 'pml_hybrid', 'pml_quad',
                  'sirt', 'tv', 'grad', 'tikh']

    for algorithm in algorithms:
        rec = tomopy.recon(data[:, slice_start:slice_end, :], theta=theta, center=rot_center, algorithm=algorithm)
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        fname_out_tiff = os.path.join(get_last_folder(sample_name), f"tomopy_{algorithm}/")
        os.makedirs(fname_out_tiff, exist_ok=True)
        LOGGER.info(f"Saving slices in '{fname_out_tiff}'")
        dxchange.write_tiff_stack(rec[:, :, :], fname=fname_out_tiff + 'slice')
        LOGGER.info("Slices saved successfully")

    '''

    LOGGER.debug("START RECONSTRUCTION")
    rec = tomopy.recon(data[:, slice_start:slice_end, :], theta=theta, center=rot_center, algorithm='gridrec')
    LOGGER.debug(f"END RECONSTRUCTION")
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)



    # save slices in tiff format
    fname_out_tiff = os.path.join(get_last_folder(sample_name), f"tomopy_{algorithm}/")
    os.makedirs(fname_out_tiff) if not os.path.exists(fname_out_tiff) else None

    LOGGER.info(f"Saving slices in '{fname_out_tiff}'")
    dxchange.write_tiff_stack(rec[:, :, :], fname=fname_out_tiff + 'slice')
    LOGGER.info("Slices saved successfully")



    kblt_reconstruct(tomos_3d, flats_3d, sample_name, algorithm)
















def kblt_reconstruct(tomos_3d, flats_3d, sample_name, algorithm):
    tomos = kblt_normalize(tomos_3d, flats_3d)
    tomos[np.isnan(tomos)] = 0
    tomos[tomos == -np.inf] = 0
    tomos[tomos == np.inf] = 1

    # save normalized photos
    fname_out_tiff = get_last_folder(sample_name)
    normal_path = os.path.join(fname_out_tiff, "normalized")
    os.makedirs(normal_path, exist_ok=True)

    LOGGER.debug("Starting saving normals")
    for i, tomo in enumerate(tomos):
        cv.imwrite(f'{normal_path}/normal_{i}.tiff', tomo)
        LOGGER.debug(f"Saved Normal in {normal_path}/normal_{i}.tiff'")

    data = tomopy.minus_log(tomos)
   # data = np.nan_to_num(data)

    theta = tomopy.angles(data.shape[0], 0, 360)

    rot_center = (data.shape[2]) / 2.0
    LOGGER.info(f"Center of rotation image: {rot_center}")

   # auto_rot_center = tomopy.find_center_pc(data[0], data[-1], tol=0.5, rotc_guess=rot_center)
   # LOGGER.info(f"Automatically detected center of rotation: {auto_rot_center}")

    slice_start = 0
    slice_end = len(data[0])
    

    '''
    algorithms = ['art', 'bart', 'fbp', 'gridrec', 'mlem', 'osem',
                  'ospml_hybrid', 'ospml_quad', 'pml_hybrid', 'pml_quad',
                  'sirt', 'tv', 'grad', 'tikh']

    for algorithm in algorithms:
        rec = tomopy.recon(data[:, slice_start:slice_end, :], theta=theta, center=rot_center, algorithm=algorithm)
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        fname_out_tiff = os.path.join(get_last_folder(sample_name), f"kblt_{algorithm}/")
        os.makedirs(fname_out_tiff, exist_ok=True)
        LOGGER.info(f"Saving slices in '{fname_out_tiff}'")
        dxchange.write_tiff_stack(rec[:, :, :], fname=fname_out_tiff + 'slice')
        LOGGER.info("Slices saved successfully")


    '''






    LOGGER.debug("START RECONSTRUCTION")
    rec = tomopy.recon(data[:, slice_start:slice_end, :], theta=theta, center=rot_center, algorithm=algorithm)
    LOGGER.debug(f"END RECONSTRUCTION")
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)




    # save slices in tiff format
    fname_out_tiff = os.path.join(get_last_folder(sample_name), f"kblt_{algorithm}/")
    os.makedirs(fname_out_tiff) if not os.path.exists(fname_out_tiff) else None

    LOGGER.info(f"Saving slices in '{fname_out_tiff}'")
    dxchange.write_tiff_stack(rec[:, :, :], fname=fname_out_tiff + 'slice')
    LOGGER.info("Slices saved successfully")

def kblt_normalize(arr, flat, cutoff=1.0, ncore=None, out=None):
    """
    Normalize raw projection KBLT data using only the flat field projections.

    This function is a modified version of the following function from TomoPy:
    https://tomopy.readthedocs.io/en/latest/api/tomopy.prep.normalize.html#tomopy.prep.normalize.normalize

    Parameters
    ----------
    arr : ndarray
        3D stack of projections.
    flat : ndarray
        3D flat field data.
    cutoff : float, optional
        Permitted maximum vaue for the normalized data.
    ncore : int, optional
        Number of cores that will be assigned to jobs.
    out : ndarray, optional
        Output array for result. If same as arr,
        process will be done in-place.

    Returns
    -------
    ndarray
        Normalized 3D KBLT tomographic data.
    """
    arr = dtype.as_float32(arr)
    l = np.float32(1e-6)
    flat = np.mean(flat, axis=0, dtype=np.float32)

    with mproc.set_numexpr_threads(ncore):
        denom = ne.evaluate('flat')
        ne.evaluate('where(denom<l,l,denom)', out=denom)
        out = ne.evaluate('arr', out=out)
        ne.evaluate('out/denom', out=out, truediv=True)
        if cutoff is not None:
            LOGGER.debug(f"CUTOFF: {cutoff}")
            cutoff = np.float32(cutoff)
            ne.evaluate('where(out>cutoff,cutoff,out)', out=out)
    return out


def get_last_folder(sample_name):
    directory = 'output/'
    directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    filtered_directories = [d for d in directories if d.startswith(f'{sample_name}')]
    sorted_names = sorted(filtered_directories, key=lambda name: (
        name.startswith(sample_name), -int(name.split('_')[-1]) if '_' in name else 0))
    return f'output/{sorted_names[0]}/recons/'



