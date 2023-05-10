import matplotlib as mpl
import matplotlib.animation as animation 
import matplotlib.pyplot as plt
import numpy as np

#creating a subplot 
figure, axes = plt.subplots( 1 ) 

 

# ------- Defining Methods ---------
def circle_contact(circle_x, circle_y, r, ray_x, ray_y):
       if ((ray_x - circle_x)**2 + (ray_y - circle_y)**2 == r**2):
        return True;
       else:
        return False;
 
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
    {'center': np.array([15, 3]), 'radius': 3, 'focal': 20},
    {'center': np.array([200, 10]), 'radius': 10, 'focal': 20}
]
origin = np.array([2,3])





# ------- Running Code -------
# draw_circle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius'])


draw_halfcircle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius']) # lense 1

axes.scatter(origin[0],origin[1], s=15, c='g') # origin 





 

# ------- Plotting --------

plt.axhline(y = 0.03, color = '#000000', linestyle = '-', linewidth=3) #uneecessary line 
axes.set_aspect( 1 ) 
plt.xlim( 0 , 20 )
plt.ylim( 0 , 10 ) 
plt.title('Ray Tracing')
plt.show()

