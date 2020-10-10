"""
Authors: Addison Spiegel
10 colors with file choosing gui, greyscale thresholds dont really work that well
Created: 10/1
"""

import cv2
import numpy
import os.path
#  importing the gui module
import tkinter as tk
# importing the function that creates the file finder
from tkinter.filedialog import askopenfilename

# this function does nothing, it is for the creation of the cv2 createTrackbar, it requires a function as an argument
def nothing(x):
    pass
class Application(tk.Frame):
    # initializing the tkinter application
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    # creates the button to pick a file

    def create_widgets(self):
        self.quit = tk.Button(self, text="Pick a file", fg="black",
                              command=self.getFile)
        self.quit.pack(side="bottom")

    # getting the file path
    def getFile(self):
        filename_valid = False
        # keep asking for the correct file to be inputted
        while filename_valid == False:
            # the tkinter gui function
            self.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

            # checking if file path is valid
            if os.path.isfile(self.filename) == True:
                filename_valid = True
            else:

                print ("Something was wrong with that filename. Please try again.")
        self.createImage()

    def createImage(self):
        # returns a the image in rgb
        original_image = cv2.imread(self.filename,1)
        # returns the image in greyscale
        grayscale_image_simple = cv2.imread(self.filename, 0)

        # converts the greyscale image back to bgr
        grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)

        # Creates a new window on the display with the name you give it
        # cv2.namedWindow('Original Image')
        # cv2.namedWindow('Grayscale Image')
        # cv2.namedWindow('Red Parts of Image')
        # cv2.namedWindow('Yellow Parts of Image')
        cv2.namedWindow('Customized Image')
        cv2.namedWindow('sliderWindow')
        cv2.resizeWindow('sliderWindow', 300, 1500)
        cv2.namedWindow('sliderWindow1')
        cv2.resizeWindow('sliderWindow1', 300, 1500)
        # the height of the image
        image_height = original_image.shape[0]
        # the width of the image
        image_width = original_image.shape[1]
        # how many channels the image has, in this case, 3
        image_channels = original_image.shape[2]



        rgbl = ['R','G','B']

        # Creating all the trackbars, this for loop set up will make it easier in the future to make more sliders quickly
        window = "sliderWindow"
        for i in range(1,11):
            if i == 6:
                window = "sliderWindow1"
            # trackbar for grayscale threshold
            cv2.createTrackbar(f"threshold {i}", window,i*20,255,nothing)
            for a in rgbl:
                #creating the trackbar that will adjust the grayscale threshold
                cv2.createTrackbar(f"Color {i}{a}", window,i*20,255,nothing)

        while True:
            # the -1 makes it easier to put it into a for loop because it adds +1 to the first break to make it a usuable range
            breaks = [[-1,-1,-1]]
            # creating an empty image for all the papers
            papers = numpy.zeros((10,image_height, image_width, image_channels), numpy.uint8)

            # adjusting the grayscale threshold with the cv2 function that gets the position of the trackbar
            window = "sliderWindow"
            for i in range(1,11):
                if i == 6:
                    window = "sliderWindow1"
                g = cv2.getTrackbarPos(f'threshold {i}', window)

                # adding the grayscale break of the trackbars to the list
                breaks.append([g,g,g])

                # creating the solid color image within the paper array
                papers[i-1,0:image_height,0:image_width, 0:image_channels] = [cv2.getTrackbarPos(f'Color {i}B', window)
                                                                            ,cv2.getTrackbarPos(f'Color {i}G', window),
                                                                            cv2.getTrackbarPos(f'Color {i}R', window)]
            # adding this to end so that there is a color for every grayscale value
            breaks.append([255,255,255])

            # converting breaks to uint8 so that it will work with cv2
            breaks = numpy.asarray(breaks, numpy.uint8)

            blocks = []

            # creating a mask for each color that will be stored in the 'blocks' list
            for i in range(0,10):
                blocks.append(cv2.inRange(grayscale_image, breaks[i+1], breaks[i]))

            parts = []
            # applying the mask to the papers and storing this in the 'parts' list
            for i in range(0,10):
                parts.append(cv2.bitwise_or(papers[i], papers[i], mask=blocks[i]))

            # iteratively applying the blocks to the previously created image
            # essentially, will result in all the blocks being combined into the final image
            customized_image = cv2.bitwise_or(parts[0], parts[1])
            for i in range(2,10):
                customized_image = cv2.bitwise_or(customized_image, parts[i])
            # showing the image in the previously created windows
            cv2.imshow('Original Image', original_image)
            cv2.imshow('Grayscale Image',grayscale_image)
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

root = tk.Tk()
app = Application(master=root)
app.mainloop()
