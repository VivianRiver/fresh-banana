from pathlib import Path
from PIL import Image
import numpy as np

p = Path('./data/raw/224')
gen = p.rglob('*.jpg')
result_list = sorted(gen)

def get_image_label(file_name):
    part = file_name.split('_')[1]
    number_string = part[1:]
    number = int(number_string)
    return number

def get_image_array(file):
    with Image.open(file) as image:
        rgb = image.convert("RGB")
        arr = np.array(rgb)
    return arr

image_labels = [get_image_label(file.name) for file in result_list]
image_arrays = [get_image_array(file) for file in result_list]

print(image_labels[0])
print(image_arrays[0].shape)