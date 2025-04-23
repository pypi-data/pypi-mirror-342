import cv2
def get_perimeter(binary_image: np.array) -> float:
    """
    Get the perimeter of the shape in the image.

    Args:
        binary_image (np.array): A binary image with one closed shape.

    Returns:
        float: The pixel length of the perimeter of the shape
    """    
    # Ensure the image is binary
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If there are contours, return the perimeter of the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return cv2.arcLength(largest_contour, closed=True)
    
    return 0
