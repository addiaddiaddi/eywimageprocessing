"""
Authors: Addison Spiegel
Fully functioning application
-allows you to create cool filters for images
-10 colors and thresholds
-gui for file picking and saving
-saving and loading color and grayscale parameters
Created: 10/9
"""

#required for basic function of this app
import cv2
import numpy
#used to deal with the file paths
import os.path
#  importing the gui module
import tkinter as tk
# message popups
from tkinter import messagebox

# importing the function that creates the file finder

from tkinter.filedialog import askopenfilename, asksaveasfile
# random is used for randomzing parameters
import random

#used to evaluate string as list literal
import ast
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
            self.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

            # checking if file path is valid and if the file is a jpg or png
            if 'jpg' in self.filename or 'png' in self.filename:
                if os.path.isfile(self.filename) == True:
                    filename_valid = True
            else:

                print ("Something was wrong with that file. Please try again.")
        self.createImage()

    #function that creates all the trackbars
    # the list in the specified text file is the parameter
    def makeTrackbars(self, parameters=None):

        #creating the sliderwindwos and resizing them appropriately
        cv2.namedWindow('Slider Window')
        cv2.resizeWindow('Slider Window', 350, 1500)
        cv2.namedWindow('Slider Window1')
        cv2.resizeWindow('Slider Window1', 350, 1500)
        cv2.moveWindow('Slider Window',0, 0)
        cv2.moveWindow('Slider Window1',350, 0)

        rgbl = ['R','G','B']

        # Creating all the trackbars, this for loop set up will make it easier in the future to make more sliders quickly
        window = "Slider Window"

        # will randomly generate trackbar parameters if none are specified (ie, at creation)
        if parameters is None:
            for i in range(1,11):
                if i == 6:
                    window = "Slider Window1"
                cv2.createTrackbar(f"Threshold {i}", window,i*random.randrange(5,20),255,nothing)
                for a in rgbl:
                    #creating the trackbar that will adjust the grayscale Threshold
                    # random initialization value so that the picture looks decnet
                    cv2.createTrackbar(f"Color {i}{a}", window,i*random.randrange(5,20),255,nothing)
        # loading the parameters into the trackbar
        else:
            # evalutating the string list as a literal list
            parameters =  ast.literal_eval(parameters)

            for i in range(1,11):
                if i == 6:
                    window = "Slider Window1"
                #creating the trackbar with the specified value in the list
                cv2.createTrackbar(f"Threshold {i}", window,parameters[i-1][0],255,nothing)

                cv2.createTrackbar(f"Color {i}R", window,parameters[i-1][1],255,nothing)
                cv2.createTrackbar(f"Color {i}G", window,parameters[i-1][2],255,nothing)
                cv2.createTrackbar(f"Color {i}B", window,parameters[i-1][3],255,nothing)

    def createImage(self):
        # returns a the image in rgb
        original_image = cv2.imread(self.filename,1)
        # returns the image in greyscale
        grayscale_image_simple = cv2.imread(self.filename, 0)

        # converts the greyscale image back to bgr
        grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)

        # Creates a new window on the display with the name you give it
        # cv2.WINDOW_NORMAL allows you to resize the image
        cv2.namedWindow('Original Image',cv2.WINDOW_NORMAL)
        cv2.namedWindow('Grayscale Image',cv2.WINDOW_NORMAL)
        cv2.namedWindow('Customized Image',cv2.WINDOW_NORMAL)
        # cv2.namedWindow('Red Parts of Image')
        # cv2.namedWindow('Yellow Parts of Image')
        cv2.moveWindow('Customized Image',700, 0)
        cv2.moveWindow('Grayscale Image',700,700)
        cv2.moveWindow('Original Image',1500,700)



        # the height of the image
        image_height = original_image.shape[0]
        # the width of the image
        image_width = original_image.shape[1]
        # how many channels the image has, in this case, 3
        image_channels = original_image.shape[2]

        # resetting the image size to default,
        # for some reason it works better with cv2.WINDOW_NORMAL when you do this
        cv2.resizeWindow('Original Image', image_width, image_height)
        cv2.resizeWindow('Grayscale Image', image_width, image_height)
        cv2.resizeWindow('Customized Image', image_width, image_height)

        # irrelevant
        # winheight = 1000
        # if image_height > image_width:
        #     winheight = 1000
        #     winwidth = 1000 / int(winheight * image_width)
        # else:
        #     winwidth = 1000
        #     winheight = 1000 / int(winwidth * image_height)


        # creating the trackbars with random parameters
        self.makeTrackbars(parameters=None)


        while True:
            # the -1 makes it easier to put it into a for loop because it adds +1 to the first break to make it a usuable range
            breaks = [[-1,-1,-1]]
            # creating an empty image for all the colors
            papers = numpy.zeros((10,image_height, image_width, image_channels), numpy.uint8)

            # adjusting the grayscale Threshold with the cv2 function that gets the position of the trackbar
            window = "Slider Window"
            for i in range(1,11):
                if i == 6:
                    window = "Slider Window1"
                g = cv2.getTrackbarPos(f'Threshold {i}', window)

                # adding the grayscale break of the trackbars to the list
                breaks.append([g,g,g])

                # creating the solid color image within the paper array
                papers[i-1,0:image_height,0:image_width, 0:image_channels] = [cv2.getTrackbarPos(f'Color {i}B', window)
                                                                            ,cv2.getTrackbarPos(f'Color {i}G', window),
                                                                            cv2.getTrackbarPos(f'Color {i}R', window)]
            # adding this to end so that there is a color for every grayscale value
            breaks.append([255,255,255])

            # adding up the total amount of grayscale values in the list
            total = 0
            for b in breaks:
                total += b[0]

            # finding cumulative values of the grayscale values and mulitplying by 255 for use in the image
            n = 0
            for i in range(1,10):
                n = breaks[i][0] + n
                t = n / total * 255
                breaks[i] = [t,t,t]

            # converting breaks to uint8 so that it will work with cv2
            breaks = numpy.asarray(breaks, numpy.uint8)

            blocks = []
            # creating a mask for each color that will be stored in the 'blocks' list
            for i in range(0,10):
                blocks.append(cv2.inRange(grayscale_image, breaks[i]+1, breaks[i+1]))

            parts = []
            # applying the mask to the papers and storing this in the 'parts' list
            for i in range(0,10):
                parts.append(cv2.bitwise_or(papers[i], papers[i], mask=blocks[i]))

            # iteratively applying the blocks to the previously created image
            # essentially, will result in all the blocks being combined into the final image
            customized_image = cv2.bitwise_or(parts[0], parts[1])
            for i in range(2,10):
                customized_image = cv2.bitwise_or(customized_image, parts[i])
            # showing the images in the previously created windows
            cv2.imshow('Original Image', original_image)
            cv2.imshow('Grayscale Image',grayscale_image)
            cv2.imshow('Customized Image',customized_image)

            # if the 'esc' key is pressed it will close all the windows
            keypressed = cv2.waitKey(1)
            if keypressed == 27:
                cv2.destroyAllWindows()
                break
            # if s is pressed, it will save the images
            elif keypressed == ord('s'):
                # making sure the user cant save an image as some other kind of file
                files = [('JPG', '*.jpg'),
                         ('PNG', '*.png')]

                # gui save file feature
                filename = asksaveasfile(filetypes = files, defaultextension = files,initialfile='Customized Images')
                cv2.imwrite(filename.name,customized_image)
                messagebox.showinfo(title="Info", message=f"Customized image successfully saved at {filename.name}")
                filename = asksaveasfile(filetypes = files, defaultextension = files,initialfile='Greyscale Image')
                cv2.imwrite(filename.name,grayscale_image)
                messagebox.showinfo(title="Info", message=f"Grayscale image successfully saved at {filename.name}")




            # if 'c' is pressed, the user will be prompted to load in parameters
            elif keypressed == ord('c'):
                # destroying the slider windows so that they can be recreated with the specified parameters
                cv2.destroyWindow("Slider Window")
                cv2.destroyWindow("Slider Window1")
                pfilename = askopenfilename()

                # getting the data from the txt file
                with open(pfilename,"r") as txt:
                    self.makeTrackbars(txt.read())

                # letting the user know that parameters were successfuly uploade
                messagebox.showinfo(title="Info", message=f"Parameters successfully loaded into the program'")

            # if 'd' is pressed, the parameters will be saved and the user can select a location and file name
            elif keypressed == ord('d'):
                parameters = []

                window = "Slider Window"
                for i in range(1,11):
                    if i == 6:
                        window = "Slider Window1"
                    # adding the current positions of the trackbars to the list
                    parameters.append([cv2.getTrackbarPos(f'Threshold {i}', window),
                                        cv2.getTrackbarPos(f'Color {i}R', window)
                                                                                ,cv2.getTrackbarPos(f'Color {i}G', window),
                                                                                cv2.getTrackbarPos(f'Color {i}B', window)])

                pfilename = asksaveasfile() #f"Parameters {str(time.time())[-5:]}"
                # creating empty text file with the user specified name
                parameterFile = open(pfilename.name, "w")

                # writing and saving the list into the file
                parameterFile.write(str(parameters))
                parameterFile.close()

                # alerting the user that the file was saved
                messagebox.showinfo(title="Info", message=f"Parameter file successfully saved at '{pfilename.name}'")

        quit()

# running the tkinter application
root = tk.Tk()
app = Application(master=root)
app.mainloop()
