import matplotlib.pyplot as plt
import numpy as np


#------- Methods ------

def normalize(vector):
    return vector / np.linalg.norm(vector)
# normalizing a vector means preserving the direction but making it unit length 1 (to do later math with it) 
# the distance from camera (orignating point) to pixel (endpoint) = vector ?? 
# np.linalg.norm is used to calclulate the length of the vector => sqrt(x^2 + y^2)
# vector / np.linalg.norm(vector) normalizes the vector (vector math) a / ||a|| = normalized a 
# this is all done with arrays and thus are vectors 






width = 300
height = 200

camera = np.array([0, 0, 1]) #camera position in 3dimensional space
ratio = float(width) / height #ratio of the sreen height and width 
print(f"Ratio: {ratio}")
#The reason for this is simple: we want the screen to have the same aspect ratio than the actual image we want to produce. 
screen = (-1, 1/ratio, -1, -1/ratio) #left, top, right, bottom  --> the grid size of the plot 
# print(f"Screen: {screen}") 
# print(f"Screen[0]: {screen[0]}") #left
# print(f"Screen[1]: {screen[1]}") #top
# print(f"Screen[2]: {screen[2]}") #right 
# print(f"Screen[3]: {screen[3]}") # bottom


objects = [
    {'center': np.array([-0.2, 0, -1]), 'radius': 0.7}, # center: x, y, z & radius 
    {'center': np.array([0.1, -0.3, 0]), 'radius': 0.1 },
    {'center': np.array([-0.3, 0, 0]), 'radius': 0.15 }
]



image = np.zeros((height, width, 3)) # makes an area of all zeros the size of the screen, this will act as the storage for all the pixel values# 3 for rgb values ig 
# print(f"Image: {image}")



#lists all the pixel values essentially from the left to the right (width valeus) to break down the pixel values into the plot valeus 
#print(f"Linespace: {np.linspace(screen[1], screen[3], height)}") 
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        print(f"Progress: {i} / {height}")
        pixel = np.array([x,y,0]) # an array consisting of the first enumerated pixel  depth (z) = 0 because it lies on the screen which is contained in the plane formed by the x and y axes; ??? idk what this means
        origin = camera # all vectors are computed from the camera 
        direction = normalize(pixel-origin) 

plt.imsave('image.png', image)






