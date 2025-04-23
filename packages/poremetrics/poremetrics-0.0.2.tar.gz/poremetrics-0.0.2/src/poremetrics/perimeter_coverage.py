import numpy as np
def perimeter_coverage(mask):
    # Get the dimensions of the mask
    height, width = mask.shape
    mask = mask.astype(np.uint8)
    if(np.max(mask)!=255):
        mask = mask*255
    # Extract the perimeter: first and last rows, and first and last columns
    perimeter_pixels = np.concatenate([
        mask[0, :],  # Top row
        mask[-1, :],  # Bottom row
        mask[0:-1, 0],  # Left column
        mask[0:-1, -1]  # Right column
    ])
    if(mask.dtype==np.uint8):
        max_size=2**8 -1
    elif(mask.dtype==np.uint16):
        max_size=2**16 -1
    elif(mask.dtype==np.uint32):
        max_size=2**32 -1
    elif(mask.dtype==np.uint64):
        max_size=2**64 -1
    elif(mask.dtype==np.float16 or mask.dtype==np.float32 or mask.dtype==np.float64):
        max_size=2**32 -1
    else:
        raise TypeError('Mask must be an unsigned interger or float. Was type:'+str(mask.dtype))

    # Total perimeter pixels
    total_perimeter_pixels = len(perimeter_pixels)*max_size

    # Count how many of those pixels are part of the mask (assuming mask is binary 1/0)
    covered_perimeter_pixels = np.sum(perimeter_pixels)

    # Calculate the percentage of the perimeter covered by the mask
    coverage_ratio = covered_perimeter_pixels / total_perimeter_pixels if total_perimeter_pixels != 0 else 0

    return coverage_ratio