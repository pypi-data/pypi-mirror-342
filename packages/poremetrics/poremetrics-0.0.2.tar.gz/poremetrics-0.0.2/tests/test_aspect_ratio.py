from poremetrics import aspect_ratio
import numpy as np

def test_box():
    array_size = 100

    # Create a binary array filled with zeros (background)
    binary_array = np.zeros((array_size, array_size), dtype=np.uint8)

    # Define the size of the colored block and its position (center)
    block_size = 40
    center_start = (array_size - block_size) // 2
    center_end = center_start + block_size

    # Set the values in the center block to 1 (colored)
    binary_array[center_start:center_end, center_start:center_end] = 1
    assert aspect_ratio(binary_array)==1
def test_circle(): 
    radius=10
    height=100
    width = 100
    center = (height // 2, width // 2)
    Y, X = np.ogrid[:height, :width]
    dist_from_center = (Y - center[0])**2 + (X - center[1])**2
    mask = dist_from_center <= radius**2
    assert aspect_ratio(mask)==1
def test_oval(): 
    x_len=11
    y_len=21
    height=100
    width = 100
    center = (height // 2, width // 2)
    Y, X = np.ogrid[:height, :width]
    dist_from_center = ((Y - center[0])/y_len)**2 + ((X - center[1])/x_len)**2
    mask = dist_from_center <= 1
    assert aspect_ratio(mask)>=max(x_len,y_len)/min(x_len,y_len)-.1 and aspect_ratio(mask)<=max(x_len,y_len)/min(x_len,y_len)+.1  
