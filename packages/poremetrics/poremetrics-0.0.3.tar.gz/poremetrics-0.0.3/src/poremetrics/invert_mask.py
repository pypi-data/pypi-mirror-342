import numpy as np
def invert_mask(mask):
    """
    Invert a binary mask (0 and 255) by swapping background and foreground.
    Parameters:
        mask (np.ndarray): 2D numpy array representing a binary mask, 
                        expected to have values either 0 or 255.

    Returns:
        np.ndarray: Inverted mask.
    """
    if not isinstance(mask, np.ndarray):
        raise TypeError("Input must be a numpy array.")

    if mask.ndim != 2:
        raise ValueError("Input mask must be a 2D array.")

    # Ensure mask is uint8
    mask = mask.astype(np.uint8, copy=False)

    # Invert the mask
    inverted = 255 - mask
    return inverted