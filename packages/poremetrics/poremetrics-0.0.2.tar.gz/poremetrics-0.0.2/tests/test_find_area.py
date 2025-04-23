from poremetrics import pixel_area
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
    binary_array[center_start:center_end, center_start:center_end] = 255
    assert pixel_area(binary_array)==(block_size**2/array_size**2)
