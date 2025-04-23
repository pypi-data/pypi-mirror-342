import numpy as np
def find_area(mask: np.ndarray) -> float:
    """
    Finds the portion of pixels taken up by the mask.

    Args:
        mask (np.ndarray): Should be a binary imagewith dtype uint8, which gives a pixel value of 255.

    Returns:
        float: The portion of the image taken up by the mask. Range of [0,1].
    """
    return float(np.sum(mask) / (mask.size*255))
