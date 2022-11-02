from PIL import Image
from numpy import asarray

# convert to grayscale
img = Image.open('test_images/test_8.jpeg').convert('L')

# reduce resolution
img = img.resize((24,18))

# convert to 2D array
img_array = asarray(img)
dimensions = img_array.shape

# set threshold for binary pixels
threshold = 200

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
