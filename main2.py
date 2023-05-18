
import matplotlib as mpl
import matplotlib.animation as animation 
import matplotlib.pyplot as plt
import math
import numpy as np



#---------- Subplot ------------
figure, axes = plt.subplots( 1 ) 
plot_x_lim = 40
plot_y_lim = 15
 


#----------- Methods ----------------
def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def refract(direction, normal, n1, n2):
    # Compute the incident angle
    cos_theta1 = -np.dot(direction, normal)
    
    # Check if the ray is entering or exiting the medium
    if cos_theta1 < 0:
        # Ray is entering the medium
        n1, n2 = n2, n1
        normal = -normal
        cos_theta1 = -cos_theta1
    
    # Compute the refracted angle using Snell's law
    sin_theta2 = (n1 / n2) * np.sqrt(1 - cos_theta1**2)
    
    # Handle total internal reflection
    if sin_theta2 > 1:
        return np.zeros_like(direction)
    
    # Compute the refracted direction vector
    direction_refracted = (n1 / n2) * direction + (n1 / n2 * cos_theta1 - np.sqrt(1 - sin_theta2**2)) * normal
    
    return direction_refracted


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

def origin_lens_reflection(o, k, frequency, lens_proportion):
    try:
        range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
        range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
    except:
        range_y1 = 1
        range_y2 = plot_x_lim
    #defining some constants
    color_pick = 0
    origin = origins[o]['center']

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
        print(f"Ray Reflected #{color_pick}")
        color_pick += 1 #increment to next color 
        
    



    # --- Drawing ----
    draw_lens(lenses[k]) # Lense
    plt.scatter(origin[0],origin[1],s=15, c='g') #origin

    return

def origin_lens_refraction(o, k, frequency,lens_proportion, n1, n2):
    try:
        range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
        range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
    except:
        range_y1 = 1
        range_y2 = plot_x_lim


    #defining some constants
    color_pick = 0
    origin = origins[o]['center']

    for i in np.linspace(range_y1,range_y2,frequency): 
        endpoint = np.array([get_circle_x_coords(lenses[k],i), i])
        direction_ray = normalize(endpoint - origin)
        draw_line(origin, endpoint, '#dbe9ff') #line conencting to center
        #From circle center to outlense (normal line)
        circle_endpoint = endpoint
        circle_origin = lenses[k]['center']
        direction_circle_normal = normalize(circle_endpoint - circle_origin)
        # draw_line(circle_origin, circle_endpoint) 

        #Refraction 
        direction_refracted = refract(direction_ray, direction_circle_normal, n1, n2)
        x_refracted_coords = []
        y_refracted_coords = []
        for j in np.linspace(-10,plot_x_lim,100): #you can put the bounds as the plot x limits
            try: 
                new_point_x = circle_endpoint[0] + j*direction_refracted[0]
                new_point_y = circle_endpoint[1] + j*direction_refracted[1]
                x_refracted_coords.append(new_point_x)
                y_refracted_coords.append(new_point_y)
            except:
                continue
        plt.plot(x_refracted_coords, y_refracted_coords, linestyle='--', c=colors[color_pick])
        print(f"Ray Refracted #{color_pick}")
        color_pick += 1 #increment to next color 
        

    # --- Drawing ----
    draw_lens(lenses[k]) # Lense
    plt.scatter(origin[0],origin[1],s=15, c='g') #origin



    return

# ------ OBJECTS --------


#----- Lense Number & Origin Number --------
# k = 0 # lense
# o = 3 # origin
# lens_proportion = 4 # what percentage of the lense do the rays cover 
# --------------------------



lenses = [
    {'center': np.array([15, 5]), 'radius': 3, 'focal': 20},
    {'center': np.array([6, 5]), 'radius': 5, 'focal': 20},
    {'center': np.array([20, 5]), 'radius': 10, 'focal': 20},
    {'center': np.array([40, 10]), 'radius': 20, 'focal': 20}
]
origins = [
    {'center': np.array([3,5])},
    {'center': np.array([15,5])},
    {'center': np.array([30,5])},
    {'center': np.array([20,15])}
]

colors = np.array(['#FFBB74','#FFE874','#E4FF74','#CAFF74', '#ABFF74', '#7FFF74', '#74FFB7','#74FFD1','#74FFF9','#74E6FF','#74CAFF', '#74ADFF', '#7491FF', '#8574FF'])




#------------ Running Reflection --------------
# origin_lens_reflection(0, 0, 10, 2)  # convex reflection
# origin_lens_reflection(1, 1, 10, 2)    # concave reflection


#------------ Running Refraction --------------
# origin_lens_refraction(0, 0, 10, 4, 1, 2)
origin_lens_refraction(0, 0, 10, 4, 1, 10)

# ------- Plotting --------

plt.axhline(y = 0.03, color = '#000000', linestyle = '-', linewidth=3) #uneecessary line 
axes.set_aspect( 1 ) 
plt.xlim( 0 , plot_x_lim )
plt.ylim( 0 , plot_y_lim ) 
plt.title('Ray Tracing')
plt.show()

