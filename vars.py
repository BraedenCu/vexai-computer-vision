import numpy as np 
import colorsys

def rgb_hsv_converter(rgb):
    (r, g, b) = rgb_normalizer(rgb)
    hsv = colorsys.rgb_to_hsv(r,g,b)
    (h,s,v) = hsv_normalizer(hsv)
    upper_bound = [h+10, s+10, v+10]
    lower_bound = [h-10, s-40, v-40]
    return upper_bound, lower_bound
def rgb_normalizer(rgb):
    (r,g,b) = rgb
    return (r/255, g/255, b/255)
def hsv_normalizer(hsv):
    (h,s,v) = hsv
    return (h*360, s*255, v*255)


#default vars
error = False
AngleValue = 0
RotationValue = 0
xOffset = 0
xRes = 1920
middleOfRes = xRes/2

#colors

l_red = np.array([150, 102, 0])
u_red = np.array([179, 204, 200])

l_green = np.array([29, 86, 6])
u_green = np.array([64, 255, 255])

#l_red = np.array([150, 102, 0])
#u_red = np.array([179, 204, 200])
#l_red = np.array([150, 102, 0])
#u_red = np.array([179, 204, 200])
