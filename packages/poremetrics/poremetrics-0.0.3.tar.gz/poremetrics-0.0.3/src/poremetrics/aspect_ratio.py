import numpy as np
def calculate_aspect_ratio(mask):
    # Find the non-zero mask coordinates
    y_coords, x_coords = np.nonzero(mask)
    
    # Calculate the bounding box dimensions
    height = int(y_coords.max()) - int(y_coords.min()) + 1
    width = int(x_coords.max()) - int(x_coords.min()) + 1
    
    # Calculate the aspect ratio
    aspect_ratio = max(width,height) / min(width,height)
    return aspect_ratio
