import matplotlib as mpl
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


# ------ OBJECTS --------
lenses = [
    {'center': np.array([15, 3]), 'radius': 3, 'focal': 20},
    {'center': np.array([200, 10]), 'radius': 10, 'focal': 20}
]
origin = np.array([2,3])





# ------- Running Code -------
# draw_circle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius'])


draw_halfcircle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius'])

axes.scatter(origin[0],origin[1], s=15, c='g')





 

# ------- Plotting --------

plt.axhline(y = 0.03, color = '#000000', linestyle = '-', linewidth=3) #uneecessary line 
axes.set_aspect( 1 ) 
plt.xlim( 0 , 20 )
plt.ylim( 0 , 10 ) 
plt.title('Ray Tracing')
plt.show()

