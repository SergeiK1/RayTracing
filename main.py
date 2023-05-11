import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

 

#creates subplots
figure, axes = plt.subplots()
axes.set_aspect('equal')

#I put this to set the scale of the plot because otherwise 
# I cannot see the circle drawn and idk how to change scale on the graph size...
x = np.array([0, 30])
print(f"X: {x}")
y = np.array([0,30])
print(f"Y: {y}")
plt.scatter(x,y)


#Draws circle 
circle = plt.Circle(( 10 , 10 ), 5 )
axes.add_artist(circle)



#Title and Show
plt.title( 'Circle' )
plt.show()

