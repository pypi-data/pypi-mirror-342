import cv2
import numpy as np
def process_mask(mask):
    # Find connected components
    num_labels, labels = cv2.connectedComponents(mask)
    
    # Count components (excluding background)
    num_objects = num_labels - 1
    
    # Find largest object
    largest_object_mask = np.zeros_like(mask)
    if num_objects > 0:
        # Get unique labels, excluding background (0)
        label_counts = [np.sum(labels == i) for i in range(1, num_labels)]
        largest_object_label = np.argmax(label_counts) + 1
        largest_object_mask = (labels == largest_object_label).astype(np.uint8) * 255
    
    return num_objects, largest_object_mask
def extract_largest_object(img,points_list):
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    for points in points_list:
        cv2.fillPoly(
            mask,
            [np.array(points, dtype=np.int32)],
            255
        )
    img_object, largest_object_mask = process_mask(mask)
    return largest_object_mask
