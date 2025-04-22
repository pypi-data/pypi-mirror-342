#Create a datatype to make euclidean distance
#created by : Anudeep Errabelly.
#Date of creation:Mon April 21 2024
import math

def compute(x1, y1, x2, y2):
    """Compute Euclidean distance between two points (x1,y1) and (x2,y2)"""
    res = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    print("Computed Euclidean Norm is below")
    print(res)
    return res


        
        
