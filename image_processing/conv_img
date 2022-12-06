from PIL import Image
import numpy as np
from numpy import asarray
import cv2

def image_to_array(image_path):

    # convert to grayscale
    img_og = Image.open(image_path)
    img = img_og.copy()
    img = img.convert('L')
    img.show()

    # reduce resolution
    img = img.resize((24,18))
    img.show()

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
    binary_img = Image.fromarray(img_array * 255 , 'L')
    binary_img.show()

def image_to_array_cv2(image_path):
    img = cv2.imread(image_path)
    resized = cv2.resize(img, (24, 18), cv2.INTER_AREA)
    cv2.imshow('sample image', resized)

    # Convert img to binary
    ret, bw_img = cv2.threshold(resized, 127, 255, cv2.THRESH_BINARY)

    #Convert to array
    binary_array = np.array(bw_img)
    print(binary_array)
    cv2.imshow("Binary", bw_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

bulk_of_path = R"C:\Users\jbrown\Documents\GitHub\tile_placer\Image Conversion\test_images"
str = bulk_of_path + r'\untiled_test.png'
image_to_array_cv2(str)
