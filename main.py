
import matplotlib.pyplot as plt
import numpy as np
import math


#---------- Subplot ------------
figure, axes = plt.subplots( 1 ) 
plot_x_lim = 80
plot_y_lim = 15



colors = np.array(['#FFBB74','#00ff44','#05dcf0','#0037ff', '#ABFF74', '#a200ff', '#74FFB7','#74FFD1','#74FFF9','#74E6FF','#74CAFF', '#74ADFF', '#7491FF', '#8574FF'])


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

def array_equals_values(arr, values):
    if len(arr) != len(values):
        return False

    for i in range(len(arr)):
        if arr[i] != values[i]:
            return False

    return True

def lens_detection(coords_object, coords_next_lens, accuracy=0.01):
    if ((abs(coords_object[0] - coords_next_lens[0]) < accuracy)) and ((abs(coords_object[1] - coords_next_lens[1])) < accuracy):
        return True
    else:
        return False


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

def origin_lens_reflection(origin, k, frequency, lens_proportion, color):
    try:
        range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
        range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
    except:
        range_y1 = 1
        range_y2 = plot_x_lim
    #defining some constants
    count = 0
    # origin = origins[o]['center']

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
        plt.plot(x_reflected_coords, y_reflected_coords, linestyle='--', c=colors[color])
        print(f"Ray Reflected #{count}")
        count += 1 #increment to next count 
        
    



    # --- Drawing ----
    draw_lens(lenses[k]) # Lense
    plt.scatter(origin[0],origin[1],s=15, c='g') #origin

    return

def origin_lens_reflection_givendirection(origin, k, frequency, lens_proportion, color, direction_ray):
    try:
        range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
        range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
    except:
        range_y1 = 1
        range_y2 = plot_x_lim
    #defining some constants
    count = 0
    # origin = origins[o]['center']

    for i in np.linspace(range_y1,range_y2,frequency): # make it in the range of the center of the circle
        # From origin to the lense
        endpoint = np.array([get_circle_x_coords(lenses[k],i), i])

        #From circle center to outlense (normal line)
        circle_endpoint = endpoint
        circle_origin = lenses[k]['center']
        direction_circle_normal = normalize(circle_endpoint - circle_origin)

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
        plt.plot(x_reflected_coords, y_reflected_coords, linestyle='--', c='r')
        print(f"Ray Reflected #{count}")
        count += 1 #increment to next count 
        
    



    # --- Drawing ----
    draw_lens(lenses[k]) # Lense
    plt.scatter(origin[0],origin[1],s=15, c='g') #origin

    return








# ________------------------______________--------

def origin_lens_refraction(origin, k, frequency,lens_proportion, n1, color):
     # --- Drawing ----
    draw_lens(lenses[k]) # Lense
    plt.scatter(origin[0],origin[1],s=15, c='g') #origin

    try:
        draw_lens(lenses[k+1])
    except:
        pass


    try:
        range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
        range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
    except:
        range_y1 = 1
        range_y2 = plot_x_lim

    
 

    #defining some constants
    n2 = lenses[k]['n']
    count = 0
    new_ray_direction_ar = []
    new_origin_ar =[]
    # origin = origins[o]['center']

    for i in np.linspace(range_y1,range_y2,frequency): 
        endpoint = np.array([get_circle_x_coords(lenses[k],i), i])
        direction_ray = normalize(endpoint - origin)
        draw_line(origin, endpoint, 'r') #line conencting to center
        #From circle center to outlense (normal line)
        circle_endpoint = endpoint
        circle_origin = lenses[k]['center']
        direction_circle_normal = normalize(circle_endpoint - circle_origin)

        try:

            next_endpoint = ((lenses[k+1]['center'][0]) - (lenses[k+1]['radius']))
        except:
            next_endpoint = plot_x_lim

        #Refraction 
        direction_refracted = refract(direction_ray, direction_circle_normal, n1, n2)
        x_refracted_coords = []
        y_refracted_coords = []
        #if the result is a 0, 0 array then it must be too high to refract so it must REFLECT 
        for j in np.linspace(0,next_endpoint - (origin[0]-1.5),1000): #you can put the bounds as the plot x limits
            try: 
                new_point_x = circle_endpoint[0] + j*direction_refracted[0]
                new_point_y = circle_endpoint[1] + j*direction_refracted[1]
                # print("Shift")
                new_coords = np.array([new_point_x, new_point_y])
                try:
                    circle_new_coords = np.array([get_circle_x_coords(lenses[k+1],new_coords[1]), new_coords[1]])
                    if lens_detection(new_coords, circle_new_coords, 0.01):
                        origin_lens_refraction_givendirection(new_coords, (k+1), frequency, lens_proportion, lenses[k]['n'], count, direction_refracted)
                        
                    else:
                        x_refracted_coords.append(new_point_x)
                        y_refracted_coords.append(new_point_y)
                        # print("else")
                    
                except:
                    # print("except")
                    x_refracted_coords.append(new_point_x)
                    y_refracted_coords.append(new_point_y)
            except:
                continue
        plt.plot(x_refracted_coords, y_refracted_coords, linestyle='--', c=colors[color])
        print(f"Ray Refracted #{count}")
        count += 1 #increment to next color 
        new_ray_direction_ar.append(direction_refracted)
        new_origin_ar.append(endpoint)


   



    return new_ray_direction_ar, new_origin_ar


#_---------------------------- Refraction given directio and stuff 
def origin_lens_refraction_givendirection(origin, k, frequency,lens_proportion, n1, color, direction_ray):
    
    # --- Drawing ----
    draw_lens(lenses[k]) # Lense
    plt.scatter(origin[0],origin[1],s=15, c='g') #origin

    try:
        draw_lens(lenses[k+1])
    except:
        pass
    
    try:
        range_y1 = lenses[k]['center'][1] - ((lenses[k]['radius'])/lens_proportion)
        range_y2 = lenses[k]['center'][1] + ((lenses[k]['radius'])/lens_proportion)
    except:
        range_y1 = 1
        range_y2 = plot_x_lim
    # print("RUNNING THE SECOND REFRACTION -----------------------------")

    #defining some constants
    n2 = lenses[k]['n']
    count = 0
    new_ray_direction_ar = []
    new_origin_ar =[]

    for i in np.linspace(range_y1,range_y2,frequency): 
        endpoint = origin
        
        try:
            next_endpoint = ((lenses[k+1]['center'][0]) - (lenses[k+1]['radius']))
        except:
            next_endpoint = plot_x_lim
        circle_origin = lenses[k]['center']
        
        direction_circle_normal = normalize(origin - circle_origin)

        #Refraction 
        direction_refracted = refract(direction_ray, direction_circle_normal, n1, n2) # ISSUE HERE IM PRETTY SURE THIS IS PRODUCING ZEROS 
        x_refracted_coords = []
        y_refracted_coords = []
        
        zero_array= np.array([0,0])
        if array_equals_values(direction_refracted, zero_array):
            print("!!!!!!!!!!REFLECT!!!!!!!!!!!!!!")
            # origin_lens_reflection_givendirection(origin, k, frequency, lens_proportion, color, direction_ray)
            #FIX REFLECTION


        for j in np.linspace(0,next_endpoint-(origin[0]-2),1000): #!!!!!!FIX ENDPOITNS TO DRAW ONLY TO THE NEXT LENSE
            try: 
                new_point_x = origin[0] + j*direction_refracted[0]
                new_point_y = origin[1] + j*direction_refracted[1]
                
                # print("Shift")
                new_coords = np.array([new_point_x, new_point_y])
                # print(f"New Coords: {new_coords}")
                try:
                    circle_new_coords = np.array([get_circle_x_coords(lenses[k+1],new_coords[1]), new_coords[1]])
                    if lens_detection(new_coords, circle_new_coords, 0.01):
                        # print(f"New Coord: {new_coords}")
                        # print(f"K+1: {k+1}")
                        # print(f"frequency: {frequency}")
                        # print(f"Lenses[k+1]['n']: {lenses[k+1]['n']}")
                        # print(f"Count: {count}")
                        color += 1
                        origin_lens_refraction_givendirection(new_coords, (k+1), frequency, lens_proportion, lenses[k]['n'], count, direction_refracted)
                        # print("new lense detected")
                    else:
                        x_refracted_coords.append(new_point_x)
                        y_refracted_coords.append(new_point_y)
                        # print("else")
                    
                except:
                    # print("except")
                    x_refracted_coords.append(new_point_x)
                    y_refracted_coords.append(new_point_y)
            except:
                continue
        plt.plot(x_refracted_coords, y_refracted_coords, linestyle='dashdot', c=colors[color])
        print(f"Ray Refracted #{count}")
        count += 1 #increment to next color 
        new_ray_direction_ar.append(direction_refracted)
        new_origin_ar.append(endpoint)

    return new_ray_direction_ar, new_origin_ar
















# ______________________________ CISI CODE _______________________________________________

lensi = []


# ------- Defining Methods ---------
def draw_circle(x,y,r,c):
    angle = np.linspace( 0 , 2 * np.pi , 150 ) 
    x_res = x + r * np.cos( angle ) 
    y_res = y + r * np.sin( angle ) 
    axes.plot(x_res, y_res, color = c)
    
    
class lens:
    
    def __init__(self, focal, xcoordinate):
        self.focal = focal
        self.xcoordinate = xcoordinate
        
class objects:
    
    def __init__(self,coordinates):
        self.coordinates = coordinates
        self.xcoordinate = coordinates[0]
        self.ycoordinate = coordinates[1]
        self.prev_ycoordinate = 0
        
    
    def trace(self,lens,colorr):
        try:
            new_xcoordinate = lens.xcoordinate + ((lens.focal * (lens.xcoordinate - self.xcoordinate)) / ((lens.xcoordinate - self.xcoordinate) - lens.focal))
            if np.isnan(new_xcoordinate):
                new_xcoordinate = lens.xcoordinate + lens.focal
            
        except:
            new_xcoordinate = math.inf
        
        new_ycoordinate = (self.ycoordinate * ((lens.xcoordinate - new_xcoordinate) / (lens.xcoordinate - self.xcoordinate)))
            
            
        draw_circle(new_xcoordinate, new_ycoordinate, 5, colorr)
        if not np.isnan(new_ycoordinate):
            print(f"Image at {new_xcoordinate} with a height of {new_ycoordinate}")
        
        if not np.isnan(new_ycoordinate) and abs(new_xcoordinate) != math.inf:
            
            first_x_values = [self.xcoordinate, new_xcoordinate]
            first_y_values = [self.ycoordinate, new_ycoordinate]
            
            second_x_values_one = [self.xcoordinate, lens.xcoordinate]
            second_y_values_one = [self.ycoordinate, self.ycoordinate]
            second_x_values_two = [lens.xcoordinate, new_xcoordinate]
            second_y_values_two = [self.ycoordinate, new_ycoordinate]
            
            third_x_values_one = [new_xcoordinate, lens.xcoordinate]
            third_y_values_one = [new_ycoordinate, new_ycoordinate]
            third_x_values_two = [lens.xcoordinate, self.xcoordinate]
            third_y_values_two = [new_ycoordinate, self.ycoordinate]
            
            plt.plot(first_x_values, first_y_values, linestyle="--", color = colorr)
            plt.plot(second_x_values_one, second_y_values_one, linestyle="--", color = colorr)
            plt.plot(second_x_values_two, second_y_values_two, linestyle="--", color = colorr)
            plt.plot(third_x_values_one, third_y_values_one, linestyle="--", color = colorr)
            plt.plot(third_x_values_two, third_y_values_two, linestyle="--", color = colorr)
            
            da_line_x = [new_xcoordinate, new_xcoordinate]
            da_line_y = [new_ycoordinate, 0]
            plt.plot(da_line_x, da_line_y, color = colorr)
            
            
        
        self.ycoordinate = new_ycoordinate
        self.coordinates = [new_xcoordinate, new_ycoordinate]
        self.xcoordinate = new_xcoordinate
        





















#----------------- INPUT FIELDS AND STUFF -----------------------


pick = str(input("Algebraic (a) or geometric (g): "))


if pick == "g":
    # -------------------- Geometric ---------------------------
    inputting = True
    lenses = []
    while inputting:
        reflect_refract = int(input("Would you like to Reflect (0) or Refract (1): "))
        if reflect_refract == 0:
            print("\n----------------------------- REFLECTING -----------------------------")
            print("---- Origin ----")
            new_origin_center_x = float(input("New Origin Coordinate X: "))
            new_origin_center_y = float(input("New Origin Coordinate Y: "))
            print("\n---- Lens ----")
            bigger = True
            while bigger:
                new_lens_center_x = float(input("New Lense Coordinate X: "))
                try:
                    if new_lens_center_x <= new_origin_center_x:
                        print("!!! The lens must be on the right side of the origin")
                        continue
                    else:
                        bigger = False
                        pass

                except:
                    bigger = False
                    pass
            new_lens_center_y = float(input("New Lens Coordinate Y: "))
            new_lens_radius = float(input("New Lens Radius: "))

            print("\n---- Concavity ----")
            convex_concave = int(input("Convex (0)  Concave (1): "))
        
            if convex_concave == 1:
                new_lens_center_x = plot_x_lim - new_lens_center_x
                new_origin_center_x = plot_x_lim - new_origin_center_x
                
            new_origin_center = np.array([new_origin_center_x, new_origin_center_y])

            lenses = [
                {
                    'center': np.array([new_lens_center_x, new_lens_center_y]), 
                    'radius': new_lens_radius
                
                }
            ]
            origin_lens_reflection(new_origin_center, 0, 10, 2, 3)  # convex reflection
            inputting = False
            break
        elif reflect_refract == 1: 

            inputting_lenses = 'y'
            counter = 0

            print("\n----------------------------- REFRACTING -----------------------------")
            print("---- Origin ----")
            new_origin_center_x = float(input("New Origin Coordinate X: "))
            new_origin_center_y = float(input("New Origin Coordinate Y: "))
            new_origin_center = np.array([new_origin_center_x, new_origin_center_y])
            print("\n---- Lens ----")
            while inputting_lenses == 'y':
                print(f"\nLens #{counter}")
        
                bigger = True
                while bigger:
                    bigger2 = True
                    while bigger2:
                        new_lens_center_x = float(input("New Lense Coordinate X: "))
                        try:
                            if new_lens_center_x <= new_origin_center_x:
                                print("!!! The lens must be on the right side of the origin")
                                continue
                            else:
                                bigger2 = False
                                pass

                        except:
                            bigger2 = False
                            pass

                    # new_lens_center_x = float(input("New Lense Coordinate X: "))
                    try:
                        if new_lens_center_x <= (lenses[counter - 1]['center'][0]+((lenses[counter - 1]['radius'])/2)) -1:
                            print("!!! The new lens must be farther than the previous lens")
                            continue
                        else:
                            bigger = False
                            pass

                    except:
                        bigger = False
                        pass

                new_lens_center_y = float(input("New Lense Coordinate Y: "))
                new_lens_radius = float(input("New Lense Radius: "))
                new_lens_refraction_index = float(input("New Lense Refraction Index: "))

                counter += 1
                
                lensi.append(
                    {
                        'center': np.array([new_lens_center_x, new_lens_center_y]), 
                        'radius': new_lens_radius,
                        'n': new_lens_refraction_index
                    },
                    )
                inputting_lenses = input("Continue? y / n: ")
            origin_lens_refraction(new_origin_center, 0, 5, 3, 1, 3 )
            inputting = False
            break
        else: 
            print("Please Select 0 or 1")
            continue
    # ------- Plotting --------
    plt.axhline(y = 0.03, color = '#000000', linestyle = '-', linewidth=3) #uneecessary line 
    axes.set_aspect( 1 ) 
    plt.xlim( 0 , plot_x_lim )
    plt.ylim( 0 , plot_y_lim ) 
    plt.title('Ray Tracing')
    plt.show()



elif pick == "a":
    # ------------------- Algebraic ---------------------------
    while True:
        try:
            num_of_lenses = int(input("How Many Lenses Would You Like to Work With? (Max of 6): "))
            if num_of_lenses > 6:
                raise Exception("bad")
            break
        except:
            print("Error: Please Enter a Valid Number of Lenses")
            continue

    lensi = []

    for i in range (1,num_of_lenses + 1):
        while True:
            if i == 1:
                fl = (input(f"What is the Focal Length of the {i}st Lens: "))
            elif i == 2:
                fl = (input(f"What is the Focal Length of the {i}nd Lens: "))
            elif i == 3:
                fl = (input(f"What is the Focal Length of the {i}rd Lens: "))
            else:
                fl = (input(f"What is the Focal Length of the {i}th Lens: "))   
            try:
                fl = float(fl)
                break
            except:
                continue
            try:
                fl = int(fl)
                break
            except:
                print("Please Enter a Numeric Focal Length")
        
        while True:
            
            if i == 1:
                xc = (input(f"What is the X-Coordinate of the {i}st Lens: "))
            elif i == 2:
                xc = (input(f"What is the X-Coordinate of the {i}nd Lens: "))
            elif i == 3:
                xc = (input(f"What is the X-Coordinate of the {i}rd Lens: "))
            else:
                xc = (input(f"What is the X-Coordinate of the {i}th Lens: "))
                
            try:
                xc = float(xc)
                break
            except:
                continue
                
            try:
                xc = int(xc)
                break
            except:
                print("Please Enter a Numeric X-Coordinate")

        current_lens = lens(fl,xc)
        lensi.append(lens(fl,xc))
        print(f'Lens {i}: Focal Length - {current_lens.focal} X-Coordinate - {current_lens.xcoordinate}')
        

    while True:
        obj1_x = input("What is the X-Coordinate of the Object: ")
        try:
            obj1_x = float(obj1_x)
            break
        except:
            continue
        try:
            obj1_x = int(obj1_x)
            break
        except:
            print('Error: Please Enter a Numerical X-Coordinate')


    while True:
        obj1_y = input("What is the Y-Coordinate of the Object: ")
        try:
            obj1_y = float(obj1_y)
            break
        except:
            continue
            
        try:
            obj1_y = int(obj1_y)
            break
        except:
            print('Error: Please Enter a Numerical Y-Coordinate')

    xbound = 600
    ybound = 150
    lens1 = lens(20, 40)
    obj1 = objects([obj1_x, obj1_y])
    draw_circle(obj1_x, obj1_y,5,"black")

    og_x = [obj1_x, obj1_x]
    og_y = [obj1_y, 0]
                
    plt.plot(og_x, og_y, color = "black")
    




    # ------- Running Code -------



    col = 0
    for j in lensi:
        
        if abs(obj1.ycoordinate) != math.inf:   
            obj1.prev_ycoordinate = obj1.ycoordinate
        obj1.trace(j, colors[col])
        if np.isnan(obj1.ycoordinate):
            print(obj1.prev_ycoordinate)
            obj1.ycoordinate = -obj1.prev_ycoordinate *(j.focal / previous_lens.focal)
            print(f"Image at {obj1.xcoordinate} with a height of {obj1.ycoordinate}")
        previous_lens = j
        col = col + 1





    # ------- Plotting --------

    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

    for k in lensi:
        plt.plot([k.xcoordinate, k.xcoordinate], [(-1 * ybound), ybound], color = 'black', linestyle = '--')

    plt.plot([obj1.xcoordinate],[obj1.ycoordinate], marker = 'o', markersize = 3, color = 'red')

    axes.set_aspect( 1 ) 
    plt.xlim( (-1 * xbound) , xbound )
    plt.ylim( (-1 * ybound) , ybound ) 

    plt.title('Ray Tracing')
    plt.show()




# IFFF IT ERRRORS TRY RESIZING WINDOW !!!!!! 
#GOOD TEST

# lenses = [
#     {'center': np.array([20, 7.5]), 'radius': 10, 'n': 1.3},
#     {'center': np.array([30, 7.5]), 'radius': 10, 'n': 2.5},
#     {'center': np.array([40, 7.5]), 'radius': 10, 'n': 3.5},
#     {'center': np.array([60, 7.5]), 'radius': 10, 'n': 2}
# ]
# origins = [
#     {'center': np.array([1,7.5])},






