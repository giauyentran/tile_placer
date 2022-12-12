from PIL import Image
import numpy as np
from numpy import asarray

def image_to_array(image_path):

    # convert to grayscale
    img = Image.open(image_path)
    img = img.convert('L')
    xdim = 24
    ydim = 18
    #img.show()

    # reduce resolution
    img = img.resize((xdim, ydim))
    #img.show()

    # convert to 2D array
    img_array = np.array(img)
    dimensions = img_array.shape

    # set threshold for binary pixels
    threshold = 125

    # convert to binary array
    for j in range(dimensions[1]):
        for i in range(dimensions[0]):
            if img_array[i][j] >= threshold:
                img_array[i][j] = 1
            else:
                img_array[i][j] = 0

    # convert array into binary array
    #binary_img = Image.fromarray(img_array * 255, 'L')
    #binary_img.show()

    return img_array