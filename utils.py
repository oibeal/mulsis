import math

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
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return math.degrees(math.atan2(changeInY,changeInX))