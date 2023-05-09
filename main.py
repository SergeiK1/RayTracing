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


# ------ Lenses --------
lenses = [
    {'center': np.array([4, 3]), 'radius': 2, 'focal': 20},
    {'center': np.array([200, 10]), 'radius': 10, 'focal': 20}
]





# ------- Running Code -------

draw_circle(lenses[0]['center'][0],lenses[0]['center'][1], lenses[0]['radius'])







 

# ------- Plotting --------

plt.axhline(y = 0.1, color = 'r', linestyle = '-')
axes.set_aspect( 1 ) 
axis_size = 10
plt.xlim( 0 , axis_size )
plt.ylim( 0 , axis_size ) 
plt.title('Ray Tracing')
plt.show()

