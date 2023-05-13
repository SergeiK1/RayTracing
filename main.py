import matplotlib as mpl
import matplotlib.animation as animation 
import matplotlib.pyplot as plt
import numpy as np

#creating a subplot 
figure, axes = plt.subplots( 1 ) 
plot_x_lim = 20
plot_y_lim = 10
 

# ------- Defining Methods ---------
def circle_contact(circle_x, circle_y, r, ray_x, ray_y):
       if ((ray_x - circle_x)**2 + (ray_y - circle_y)**2 <= r**2):
        return True;
       else:
        return False;

def get_circle_x_coords(h, k, radius, y_value):
    # h, k = center (x,y)
    print(f"Circle x_coord Input: {h,k,radius,y_value}")
    x_value = np.sqrt(radius**2 - (y_value - k)**2) + h
    x_value2 = h-(x_value-h)
    return x_value, x_value2
 
def draw_circle(x,y,r):
   angle = np.linspace( 0 , 2 * np.pi , 150 ) 
   x_res = x + r * np.cos( angle ) 
   y_res = y + r * np.sin( angle ) 
   axes.plot(x_res, y_res)

def draw_halfcircle(x,y,r):
   angle = np.linspace( 2*(np.pi)/3 , 4*(np.pi)/3 , 150 ) #not true half circle --> change the numbers around pi to make it truly half 
   x_res = x + r * np.cos( angle ) 
   y_res = y + r * np.sin( angle ) 
   axes.plot(x_res, y_res)


# fix for the closest interspet (convert to 2d)

# def nearest_intersected_object(objects, ray_origin, ray_direction):
#     distances = [sphere_intersect(obj['center'], obj['radius'], ray_origin, ray_direction) for obj in objects]
#     nearest_object = None
#     min_distance = np.inf
#     for index, distance in enumerate(distances):
#         if distance and distance < min_distance:
#             min_distance = distance
#             nearest_object = objects[index]
#     return nearest_object, min_distance


# ------ OBJECTS --------
lenses = [
    {'center': np.array([13, 3]), 'radius': 3, 'focal': 20},
    {'center': np.array([10, 5]), 'radius': 3, 'focal': 20},
    {'center': np.array([200, 10]), 'radius': 10, 'focal': 20}
]
origin = np.array([2,4])





# ------- Running Code -------
# draw_circle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius'])

# Draw objects and lenses
draw_halfcircle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius']) # lense 1
# draw_halfcircle(lenses[1]['center'][0],lenses[1]['center'][1], lenses[1]['radius']) # lense 2
axes.scatter(origin[0],origin[1], s=15, c='g') # origin 

# print(get_circle_x_coords(lenses[0]['center'][0],lenses[0]['center'][1] , lenses[0]['radius'], origin[1])) # lense 1 x coords
# print(get_circle_x_coords(lenses[1]['center'][0],lenses[1]['center'][1] , lenses[1]['radius'], origin[1])) # lense 2 x coords
print(f"Result: {get_circle_x_coords(lenses[0]['center'][0],lenses[0]['center'][1] , lenses[0]['radius'], origin[1])[1]}")

#run a loop that tests iterates the x coordinate until it detects the circle

circle_x = lenses[0]['center'][0]
circle_y = lenses[0]['center'][1]
r = lenses[0]['radius']


frequency = 1000
for i in np.linspace(0,plot_x_lim,frequency): #checks frequency amount of points between the two bounds of the graph 
   if circle_contact(circle_x, circle_y, r, i, origin[1]):
      contact = np.array([i, origin[1]])
      plt.plot(np.linspace(origin[0],contact[0],100),np.full_like(np.linspace(origin[0],contact[0],100), origin[1]), color="r") #plots the line from origin to the lense
      print('-------------------------')
      print(f"Contact: {contact}")
      break
   else: 
      print(i)



 

# ------- Plotting --------

# plt.plot(np.linspace(0,20,100),np.full_like(np.linspace(0,20,100), origin[1]))

plt.axhline(y = 0.03, color = '#000000', linestyle = '-', linewidth=3) #uneecessary line 
axes.set_aspect( 1 ) 
plt.xlim( 0 , plot_x_lim )
plt.ylim( 0 , plot_y_lim ) 
plt.title('Ray Tracing')
plt.show()

