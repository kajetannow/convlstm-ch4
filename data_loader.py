import os
import numpy as np
# import cv2
from skimage.transform import resize
from osgeo import gdal


def read_geotiff(filename):
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    return arr, ds


def load_and_resize_tiff(filename, target_size=(64, 64)):
    arr, ds = read_geotiff(filename)
    ch4 = arr / 255
    ch4_resized = resize(ch4, target_size, anti_aliasing=True)
    return ch4_resized

def stack_sequences(data, sq_len=20):
    data = np.expand_dims(data, axis=1)
    sq_num = data.shape[0] - sq_len + 1
    sequences = np.zeros((sq_num, sq_len, 1, 64, 64))

    for i in range(sq_num):
        sequences[i] = data[i:i+sq_len]
    
    return sequences


def load_daily_ch4_dataset(location="Poznan"):
    data_dir = f"./data/output_copernicus/{location}/"
    data = []
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".tiff"):
            filepath = os.path.join(data_dir, filename)
            ch4_resized = load_and_resize_tiff(filepath)
            data.append(ch4_resized)
    #np_data = np.array(data)
    np_data = stack_sequences(data)
    np.save(f"./data/input_convlstm/CH4_stacked_{location}.npy", np_data)
    return np_data


def load_monthly_ch4_dataset(location="Poznan"):
    data_dir = "./ch4_montly_data/"
    data = []
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".tiff"):
            filepath = os.path.join(data_dir, filename)
            ch4_resized = load_and_resize_tiff(filepath)
            data.append(ch4_resized)
    return np.array(data)


data = load_daily_ch4_dataset()
print(data.shape)
