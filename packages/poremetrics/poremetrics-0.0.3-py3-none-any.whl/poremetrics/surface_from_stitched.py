import cv2
import numpy as np
def surface_from_stitched(img_path,input_size = 1024):
    all_points = []
    input_label = []
    image = cv2.resize(cv2.imread(img_path),(input_size,input_size), interpolation = cv2.INTER_AREA)
    if(input_size==1024):
        image = image[0:960,:]
        input_size = 960
    image_blurred = cv2.blur(cv2.blur(image,(6,6)),(10,10))
    condition_img = image_blurred>253
    non_zero_indices = np.nonzero(np.where(condition_img,1,0))
    #Remove reflective edges
    condition_img = image_blurred>253
    non_zero_indices = np.nonzero(np.where(condition_img,1,0))
    # if len(non_zero_indices[0]) > 0:
    #     for i in range(RANDOM_POSITIONS):
    #         temp_idx = int(random.random()*len(non_zero_indices[0]))
    #         all_points.append([non_zero_indices[1][temp_idx],non_zero_indices[0][temp_idx]])
    #         input_label.append(0)

    for x_pos in [len(image_blurred[0])*.65,len(image_blurred[0])*.5,len(image_blurred[0])*.35]:
        for y_pos in [len(image_blurred[1])*.65,len(image_blurred[0])*.5,len(image_blurred[1])*.35]:
            all_points.append([x_pos,y_pos])
            input_label.append(1)

    predictor.set_image(image)
    masks, scores, logits = predictor.predict(
        point_coords=np.array(all_points),
        point_labels=np.array(input_label),
        multimask_output=False,
    )
    processed_mask = (masks[0]).astype(np.uint8) * 255

    # Step 1: Label connected components
    num_labels, labels_im = cv2.connectedComponents(processed_mask)

    # Step 2: Count pixels for each label
    sizes = np.bincount(labels_im.ravel())

    # Step 3: Find the largest component (ignore the background)
    largest_component_label = sizes[1:].argmax() + 1  # +1 to offset background

    # Step 4: Create a new mask for the largest component
    largest_defect_mask = np.zeros_like(processed_mask)
    largest_defect_mask[labels_im == largest_component_label] = 255
    processed_mask = largest_defect_mask
    # Creating kernel 
    dilate_kernel = np.ones((6, 6), np.uint8)
    erosion_kernal = np.ones((6, 6), np.uint8)
    # Using cv2.erode() method  
    processed_mask = cv2.dilate(processed_mask, dilate_kernel, cv2.BORDER_REFLECT) #
    # processed_mask = cv2.dilate(processed_mask, dilate_kernel, cv2.BORDER_REFLECT) #
    # processed_mask = cv2.dilate(processed_mask, dilate_kernel, cv2.BORDER_REFLECT) #
    processed_mask = cv2.erode(processed_mask, erosion_kernal, cv2.BORDER_REFLECT) 
    processed_mask = cv2.erode(processed_mask, erosion_kernal, cv2.BORDER_REFLECT) 
    processed_mask = cv2.erode(processed_mask, erosion_kernal, cv2.BORDER_REFLECT) 
    processed_mask = cv2.erode(processed_mask, erosion_kernal, cv2.BORDER_REFLECT) 
    processed_mask = cv2.erode(processed_mask, erosion_kernal, cv2.BORDER_REFLECT) 
    processed_mask = cv2.dilate(processed_mask, np.ones((30, 30), np.uint8), cv2.BORDER_REFLECT) #
    return processed_mask