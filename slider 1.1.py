"""
Commented original code to determine what each segment does
Author: EYW and Addison Spiegel

Created: 9/21
"""

import cv2
import numpy
import os.path

# this function does nothing, it is for the creation of the cv2 createTrackbar, it requires a function as an argument

def nothing(x):
    pass

print ("Save your original image in the same folder as this program.")
filename_valid = False
# keep asking for the correct file to be inputted
while filename_valid == False:
    filename = input("Enter the name of your file, including the "\
                                 "extension, and then press 'enter': ")
    if os.path.isfile(filename) == True:
        filename_valid = True
    else:
        print ("Something was wrong with that filename. Please try again.")

# returns a the image in rgb
original_image = cv2.imread(filename,1)
# returns the image in greyscale
grayscale_image_simple = cv2.imread(filename, 0)

# converts the greyscale image back to bgr
grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)

# Creates a new window on the display with the name you give it
# cv2.namedWindow('Original Image')
# cv2.namedWindow('Grayscale Image')
# cv2.namedWindow('Red Parts of Image')
# cv2.namedWindow('Yellow Parts of Image')
cv2.namedWindow('Customized Image')
cv2.namedWindow('sliderWindow')

# the height of the image
image_height = original_image.shape[0]
# the width of the image
image_width = original_image.shape[1]
# how many channels the image has, in this case, 3
image_channels = original_image.shape[2]

#creating the trackbar that will adjust the grayscale threshold
cv2.createTrackbar("threshold", "sliderWindow",100,255,nothing)
while True:

    # adjusting the grayscale threshold with the cv2 function that gets the position of the trackbar
    grayscale_break = cv2.getTrackbarPos('threshold', 'sliderWindow')

    # creating an empty image for the red and yellow images
    red_paper = numpy.zeros((image_height,image_width,image_channels), numpy.uint8)
    yellow_paper = numpy.zeros((image_height,image_width,image_channels),
                               numpy.uint8)

    # changing every pixel in the red image to red
    red_paper[0:image_height,0:image_width, 0:image_channels] = [0,0,255]
    # changing every pixel in the yellow image to yellow
    yellow_paper[0:image_height,0:image_width, 0:image_channels] = [0,255,255]


    #making the range of greyscales
    min_grayscale_for_red = [0,0,0]
    max_grayscale_for_red = [grayscale_break,grayscale_break,grayscale_break]
    min_grayscale_for_yellow = [grayscale_break+1,grayscale_break+1,
                                grayscale_break+1]
    max_grayscale_for_yellow = [255,255,255]

    # converting these arrays to numpy arrays
    min_grayscale_for_red = numpy.array(min_grayscale_for_red, dtype = "uint8")
    max_grayscale_for_red = numpy.array(max_grayscale_for_red, dtype = "uint8")
    min_grayscale_for_yellow = numpy.array(min_grayscale_for_yellow,
                                           dtype = "uint8")
    max_grayscale_for_yellow = numpy.array(max_grayscale_for_yellow,
                                           dtype = "uint8")

    # returns a mask that is made up of pure black and white pixels.
    # Converts grayscale pixels within the range of the two arguments
    # All the red parts turn white
    block_all_but_the_red_parts = cv2.inRange(grayscale_image,
                                              min_grayscale_for_red,
                                              max_grayscale_for_red)

    # converts all the yellow parts of the image to white
    block_all_but_the_yellow_parts = cv2.inRange(grayscale_image,
                                                 min_grayscale_for_yellow,
                                                 max_grayscale_for_yellow)
    # applies the mask onto the solid red and yellow images
    # the black from the previous 'block' variables goes on top of the solid red and yellow images
    red_parts_of_image = cv2.bitwise_or(red_paper, red_paper,
                                        mask = block_all_but_the_red_parts)

    yellow_parts_of_image = cv2.bitwise_or(yellow_paper, yellow_paper,
                                           mask = block_all_but_the_yellow_parts)

    # combines the two images, the black part on the yellow image is merged with the red from the other image
    customized_image = cv2.bitwise_or(red_parts_of_image, yellow_parts_of_image)

    # showing the image in the previously created windows
    #cv2.imshow('Original Image', original_image)
    #cv2.imshow('Grayscale Image',grayscale_image)
    #cv2.imshow('Red Parts of Image',red_parts_of_image)
    #cv2.imshow('Yellow Parts of Image',yellow_parts_of_image)
    cv2.imshow('Customized Image',customized_image)

    # if the key is pressed it will close all the windows
    keypressed = cv2.waitKey(1)
    if keypressed == 27:
        cv2.destroyAllWindows()
        break
    # if s is pressed, it will save the images
    elif keypressed == ord('s'):
        cv2.imwrite('photo_GS_1.jpg',grayscale_image)
        cv2.imwrite('photo_RY_1.jpg',customized_image)
        cv2.destroyAllWindows()
        break

quit()
