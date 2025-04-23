import cv2
def calculate_aspect_ratio_rotated(binary_image):
    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # Get the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the rotated rectangle
    rect = cv2.minAreaRect(largest_contour)
    (width, height) = rect[1]
    
    # Calculate aspect ratio (ensuring width is always the larger dimension)
    aspect_ratio = max(width, height) / min(width, height)
    
    return aspect_ratio
