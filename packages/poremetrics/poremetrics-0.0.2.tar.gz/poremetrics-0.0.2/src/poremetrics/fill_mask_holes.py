import cv2
import numpy as np

def fill_mask_holes(mask):
    """
    Fill holes in a binary mask using floodFill.
    
    Parameters:
    mask (numpy.ndarray): Binary input mask (0 and 255 values)
    
    Returns:
    numpy.ndarray: Mask with holes filled
    """
    # Ensure mask is binary and of type uint8
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    
    # Threshold to ensure binary image
    _, binary_mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    
    # Create a copy of the mask for flood filling
    # Note: floodFill needs a mask that's 2 pixels bigger in each direction
    h, w = binary_mask.shape
    filled_mask = binary_mask.copy()
    filling_mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # Flood fill from point (0,0)
    cv2.floodFill(filled_mask, filling_mask, (0,0), 255)
    
    # Invert the flood-filled image
    filled_mask_inv = cv2.bitwise_not(filled_mask)
    
    # Combine the original mask with the filled holes
    out_mask = binary_mask | filled_mask_inv
    
    return out_mask