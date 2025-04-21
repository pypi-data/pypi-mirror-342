import h5py
import numpy as np
import os
from PIL import Image
from print_hdf5_structure import print_hdf5_structure

# Make all images to a HDF5 file
def make_h5(image_dir: str, h5_path: str, image_names: list[str], image_labels, image_types):

    N = len(image_names)

    # Get image data
    image_datas = []
    for i in range(N):
        image_name = image_names[i]
        image_path = os.path.join(image_dir, image_name)
        image = Image.open(image_path).convert("RGB")
        rgb_array = np.array(image).transpose((2, 0, 1))
        image_datas.append(rgb_array)
    image_datas = np.array(image_datas, dtype=np.uint8)

    # Set train_idx = 1, 3, 5, ...
    train_idx = np.array(range(1, N, 2), dtype=np.int32)

    # Set val_idx = 0, 2, 4, ...
    val_idx = np.array(range(0, N, 2), dtype=np.int32)

    # Create a new HDF5 file
    with h5py.File(h5_path, "w") as f:
        f.create_dataset("images", data=image_datas)
        f.create_dataset("indx_train", data=train_idx)
        f.create_dataset("indx_valid", data=val_idx)
        f.create_dataset("labels", data=image_labels)
        f.create_dataset("types", data=image_types)

        # Visualize
        f.visititems(print_hdf5_structure)

__all__ = ["make_h5"]