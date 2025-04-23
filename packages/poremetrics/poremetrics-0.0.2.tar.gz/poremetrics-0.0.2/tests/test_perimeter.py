from poremetrics import perimeter
import numpy as np
import math
import skimage.draw

def test_box():
    array_size = 100

    # Create a binary array filled with zeros (background)
    binary_array = np.zeros((array_size, array_size), dtype=np.uint8)

    # Define the size of the colored block and its position (center)
    block_size = 40
    center_start = (array_size - block_size) // 2
    center_end = center_start + block_size

    # Set the values in the center block to 1 (colored)
    binary_array[center_start:center_end, center_start:center_end] = 255
    assert block_size*4*0.9<=perimeter(binary_array)<=block_size*4*1.1
def test_triangle():
    polygon = np.array([[10,10],[10,90],[50,50]])
    mask = skimage.draw.polygon2mask((100,100),polygon)
    mask = mask.astype(np.uint8)*255
    assert (2*math.sqrt(2*(40**2))+80)*0.9<=perimeter(mask)<=(2*math.sqrt(2*(40**2))+80)*1.1
