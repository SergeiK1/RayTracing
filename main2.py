
import matplotlib as mpl
import matplotlib.animation as animation 
import matplotlib.pyplot as plt
import numpy as np



#---------- Subplot ------------
figure, axes = plt.subplots( 1 ) 
plot_x_lim = 20
plot_y_lim = 10
 


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

def draw_line(origin, endpoint):
    plt.plot([origin[0], endpoint[0]], [origin[1], endpoint[1]])

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
lenses = [
    {'center': np.array([10, 3]), 'radius': 2, 'focal': 20},
    {'center': np.array([14, 4]), 'radius': 3, 'focal': 20},
    {'center': np.array([200, 10]), 'radius': 10, 'focal': 20}
]
origin = np.array([2,5])




#------ Running Code --------


for i in np.linspace(1,7,10):

    endpoint = np.array([get_circle_x_coords(lenses[1],i), i])
    direction = normalize(endpoint - origin)
    print(f"Endpoint: {endpoint}")
    print(f"Direction: {direction}")
    draw_line(origin, endpoint) #line conencting to center




# --- Drawing ----
draw_lens(lenses[1]) # Lense
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

