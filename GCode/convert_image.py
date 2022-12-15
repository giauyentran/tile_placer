from PIL import Image
import numpy as np
from numpy import asarray

def image_to_array(image_path, image_dimensions):
    '''
    Processes raw images and converts to binary array to be plotted.

    Args:
        image_path: a string denoting the image path
        image_dimensions: a 2-tuple in the form (width, height) in pixels 
            denoting the desired dimensions of the
    
    Returns a binary array of the processed image.
    '''

    # convert to grayscale
    img = Image.open(image_path)
    img = img.convert('L')
    xdim = image_dimensions[1]
    ydim = image_dimensions[0]
    img.show() # Uncomment to display grayscale image

    # reduce resolution
    img = img.resize((xdim, ydim))
    img.show() # Uncomment to display reduced grayscale image

    # convert to 2D array
    img_array = np.array(img)
    dimensions = img_array.shape

    # set threshold for binary pixels
    threshold = 150

    # convert to binary array
    for j in range(dimensions[1]):
        for i in range(dimensions[0]):
            if img_array[i][j] >= threshold:
                img_array[i][j] = 0
            else:
                img_array[i][j] = 1

    # Uncomment next 2 lines to display final binary grid
    # binary_img = Image.fromarray(img_array * 255, 'L')
    # binary_img.show()
    
    return img_array