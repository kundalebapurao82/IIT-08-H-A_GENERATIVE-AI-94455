# This module call methods to calculate area
import math_utils
# Calculate area of circle
rad = float(input("Enter radius of circle: "))
math_utils.area_of_circle(rad)


# Calculate area of square
side = float(input("Enter side of square: "))
math_utils.area_of_square(side)

# Calculate area of rectangle 
breadth = float(input("Enter breadth of rectangle: "))
width = float(input("Enter width of rectangle: "))
math_utils.area_of_rectangle(width,breadth)

# Calculate area of triangle
hight = float(input("Enter hight of triangle: "))
base = float(input("Enter base of triangle: "))
math_utils.area_of_triangle(base, hight)