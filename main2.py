
import matplotlib as mpl
import matplotlib.animation as animation 
import matplotlib.pyplot as plt
import math
import numpy as np



#---------- Subplot ------------
figure, axes = plt.subplots( 1 ) 
plot_x_lim = 35
plot_y_lim = 25
 


#----------- Methods ----------------
def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis


def normalize(vector):
    return vector / np.linalg.norm(vector)
# normalizing a vector means preserving the direction but making it unit length 1 (to do later math with it) 
# the distance from camera (orignating point) to pixel (endpoint) = vector ?? 
# np.linalg.norm is used to calclulate the length of the vector => sqrt(x^2 + y^2)
# vector / np.linalg.norm(vector) normalizes the vector (vector math) a / ||a|| = normalized a 
# this is all done with arrays and thus are vectors 

def get_circle_x_coords(lens, y_value):
    # h, k = center (x,y)
    h = lens['center'][0]
    k = lens['center'][1]
    radius = lens['radius']
    # print(f"Circle x_coord Input: {h,k,radius,y_value}")
    x_value = np.sqrt(radius**2 - (y_value - k)**2) + h
    x_value2 = h-(x_value-h)
    return min(x_value, x_value2)

def draw_line(origin, endpoint, color):
    plt.plot([origin[0], endpoint[0]], [origin[1], endpoint[1]], c=color)

def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def draw_lens(lens):
    x = lens['center'][0]
    y = lens['center'][1]
    r = lens['radius']
    angle = np.linspace( (np.pi)/2 , 3*(np.pi)/2 , 150 ) # half circle bound 
    x_res = x + r * np.cos( angle )   
    y_res = y + r * np.sin( angle ) 
    axes.plot(x_res, y_res)

# ------ OBJECTS --------


#----- Lense Number & Origin Number --------
k = 0 # lense
o = 3 # origin
lens_proportion = 4 # what percentage of the lense do the rays cover 
# --------------------------



lenses = [
    {'center': np.array([10, 10]), 'radius': 5, 'focal': 20},
    {'center': np.array([14, 4]), 'radius': 3, 'focal': 20},
    {'center': np.array([15, 10]), 'radius': 10, 'focal': 20},
    {'center': np.array([40, 10]), 'radius': 20, 'focal': 20}
]
origins = [
    {'center': np.array([5,10])},
    {'center': np.array([30,10])},
    {'center': np.array([10,6])},
    {'center': np.array([20,15])}
]
origin = origins[o]['center']
colors = np.array(['#FFBB74','#FFE874','#E4FF74','#CAFF74', '#ABFF74', '#7FFF74', '#74FFB7','#74FFD1','#74FFF9','#74E6FF','#74CAFF', '#74ADFF', '#7491FF', '#8574FF'])




#------ Running Code --------

try:
    range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
    range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
except:
    range_y1 = 1
    range_y2 = plot_x_lim

 
# range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/1.9)
# range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/1.9)

# range_y1 = 2.4
# range_y2 = 6

frequency = 14
color_pick = 0

for i in np.linspace(range_y1,range_y2,frequency): # make it in the range of the center of the circle
    # From origin to the lense
    endpoint = np.array([get_circle_x_coords(lenses[k],i), i])
    direction_ray = normalize(endpoint - origin)
    draw_line(origin, endpoint, '#dbe9ff') #line conencting to center

    #From circle center to outlense (normal line)
    circle_endpoint = endpoint
    circle_origin = lenses[k]['center']
    direction_circle_normal = normalize(circle_endpoint - circle_origin)
    # draw_line(circle_origin, circle_endpoint)

    #Reflection 
    direction_reflected = reflected(direction_ray, direction_circle_normal)
    x_reflected_coords = []
    y_reflected_coords = []
    for j in np.linspace(-10,plot_x_lim,100): #you can put the bounds as the plot x limits
        try: 
            new_point_x = circle_endpoint[0] + j*direction_reflected[0]
            new_point_y = circle_endpoint[1] + j*direction_reflected[1]
            x_reflected_coords.append(new_point_x)
            y_reflected_coords.append(new_point_y)
        except:
            continue
    plt.plot(x_reflected_coords, y_reflected_coords, linestyle='--', c=colors[color_pick])
    print(f"Ray: {color_pick}")
    color_pick += 1 #increment to next color 
    
   



# --- Drawing ----
draw_lens(lenses[k]) # Lense
plt.scatter(origin[0],origin[1],s=15, c='g') #origin




 



#------ Tets --------

# print(sphere_intersect)
# print(f"Direction: {direction}")

# ------- Plotting --------

plt.axhline(y = 0.03, color = '#000000', linestyle = '-', linewidth=3) #uneecessary line 
axes.set_aspect( 1 ) 
plt.xlim( 0 , plot_x_lim )
plt.ylim( 0 , plot_y_lim ) 
plt.title('Ray Tracing')
plt.show()

