import math
import numpy as np

def rotate_vector(vector, angle):
    angle = math.radians(angle)
    rotated_vector = [
            vector[0]*math.cos(angle) - vector[1]*math.sin(angle),
            vector[0]*math.sin(angle) + vector[1]*math.cos(angle),
        ]
    return rotated_vector

# funcion para crear circulos con canvas de Tkinter
def create_circle(x, y, r, canvasName, color): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, outline=color)

def coords_within_circle(pos_cir, pos_obj, r):
    # euclidean distance (x1-x)² + (y1-y)² <= r²
    x1 = pos_obj[0]
    y1 = pos_obj[1]
    x = pos_cir[0]
    y = pos_cir[1]
    return (x1-x)**2 + (y1-y)**2 <= r**2

def coords_within_arc(pos_cir, pos_obj, r, anglemax, anglemin):
    inside = False
    if coords_within_circle(pos_cir, pos_obj, r):
        angle = angle_btw_2_points(pos_cir, pos_obj)
        if angle <= anglemax and angle >= anglemin:
            inside = True

    return inside

def angle_btw_2_points(pointA, pointB):
    a = np.array(pointA)
    b = np.array(pointB)
    angle = calculate_rotation_angle_from_vector_to_vector(a,b)
    if angle > 180:
        angle -= 360

    return angle

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    all_zero = True
    i = 0
    while i < len(vector) and all_zero:
        if vector[i] != 0:
            all_zero = False
        
        i += 1

    if all_zero:
        return [0, 0]
    
    return vector / np.linalg.norm(vector)

def calculate_rotation_angle_from_vector_to_vector(a,b):
    """ return rotation angle from vector a to vector b, in degrees.
    Args:
        a : np.array vector. format (x,y)
        b : np.array vector. format (x,y)
    Returns:
        angle [float]: degrees. 0~360
    """
    unit_vector_1 = unit_vector(a)
    unit_vector_2 = unit_vector(b)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    angle = angle/ np.pi * 180
    c = np.cross(b,a)
    if c>0:
        angle +=180
    
    return angle

    