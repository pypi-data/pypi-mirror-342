import h5py
import numpy as np
import os
from PIL import Image
from .print_hdf5_structure import print_hdf5_structure

# Make all images to a HDF5 file
def make_h5(image_dir, h5_path, image_names = [], indx_train = None, indx_valid = None, image_labels = None, image_types = None):

    N = len(image_names)

    # Process none
    if indx_train is None:
        indx_train = np.array(range(1, N, 2), dtype=np.int32)
    if indx_valid is None:
        indx_valid = np.array(range(0, N, 2), dtype=np.int32)
    if image_labels is None:
        image_labels = np.zeros(N)
    if image_types is None:
        image_types = np.zeros(N)

    # Get image data
    image_datas = []
    for i in range(N):
        image_name = image_names[i]
        image_path = os.path.join(image_dir, image_name)
        image = Image.open(image_path).convert("RGB")
        rgb_array = np.array(image).transpose((2, 0, 1))
        image_datas.append(rgb_array)
    image_datas = np.array(image_datas, dtype=np.uint8)

    # Create a new HDF5 file
    with h5py.File(h5_path, "w") as f:
        f.create_dataset("images", data=image_datas)
        f.create_dataset("indx_train", data=indx_train)
        f.create_dataset("indx_valid", data=indx_valid)
        f.create_dataset("labels", data=image_labels)
        f.create_dataset("types", data=image_types)

        # Visualize
        f.visititems(print_hdf5_structure)

__all__ = ["make_h5"]