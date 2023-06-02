# RayTracing2
A Visual Guide to Ray Tracing used to aid in teaching

IF CODE DOESN'T SHOW RESIZE YOUR WINDOW


# Good test for refraction:

lenses = [
    {'center': np.array([20, 7.5]), 'radius': 10, 'n': 1.3},
    {'center': np.array([30, 7.5]), 'radius': 10, 'n': 2.5},
    {'center': np.array([40, 7.5]), 'radius': 10, 'n': 3.5},
    {'center': np.array([60, 7.5]), 'radius': 10, 'n': 2}
]
origins = [
    {'center': np.array([1,7.5])},
