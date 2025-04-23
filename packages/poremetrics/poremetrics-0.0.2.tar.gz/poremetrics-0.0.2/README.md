# pore-fatigue-metrics
This repo contains the source code for the poremetrics package, which provides functions which take binary numpy arratys as an input nd outputs features which can be used to predict fatigue performance in the case of defect initiated fatigue.

Note, all of the functions contained here expect a numpy array of shape (x,y), with no channels, and a format of np.uint8. This will probably require the user to reshape their images, but it removes the ambiguity arround the location of the color channels, and this is built on top of cv2 and numpy, with some cv2 functions only supporting the np.uint8 dtype.
