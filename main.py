import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

 
def circle_contact(circle_x, circle_y, r, ray_x, ray_y):
       if ((ray_x - circle_x)**2 + (ray_y - circle_y)**2 == r**2):
        return True;
       else:
        return False;
 


origin = np.array([0, 10,]) # x, y

lenses = [
    {'center': np.array([100, 10]), 'radius': 10, 'focal': 20},
    {'center': np.array([200, 10]), 'radius': 10, 'focal': 20}
]


# print(circle_contact(lenses[0]['center'][0],lenses[0]['center'][1],lenses[0]['radius'], 89, 10))





for i in range(300):
       print(i)
       if (circle_contact(lenses[0]['center'][0],lenses[0]['center'][1],lenses[0]['radius'], i, 10)):
              print("Touching")
              break
       else:
            print(i)
              