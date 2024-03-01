#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from .my_functions import get_intersection_point, reflect, rad_to_deg, deg_to_rad
from .generate_points import generate_points



def find_z(start_point, angle_to_the_axis, sphere_center, radius):
    all_x = []
    all_z = []

    all_x.append(start_point[0])
    all_z.append(start_point[2])


    direction = np.array([np.sin(angle_to_the_axis*deg_to_rad), 0, np.cos(angle_to_the_axis*deg_to_rad)])
    #print("\n direction: ", direction)

    intersection_point, outside_lens = get_intersection_point(start_point, direction, sphere_center, radius)
    if outside_lens:
        print("photon is discarded")
        return False
    #print("\n intersection_point: ", intersection_point)

    all_x.append(intersection_point[0])
    all_z.append(intersection_point[2])

    refracted_direction = reflect(direction, sphere_center, intersection_point, in_or_out='in')
    #print("\n refracted_direction: ", refracted_direction)

    second_intersection_point, useless_bool_var  = get_intersection_point(intersection_point, refracted_direction, np.array([0, 0, -1850.]), radius)
    #print("\n second_intersection_point: ", second_intersection_point)

    all_x.append(second_intersection_point[0])
    all_z.append(second_intersection_point[2])   

    second_refracted_direction = reflect(refracted_direction, np.array([0, 0, -1850.]), second_intersection_point, in_or_out='out')
    #print("\n second_refracted_direction: ", second_refracted_direction)

    #focal_distance = 1923.    # farthest  
    #focal_distance = 1808.    # at zero angle  
    #focal_distance = 1755.    # at 5  
    #focal_distance = 1665.    # at 10  
    focal_distance = 1605.    # at 12.5  


    p = (focal_distance - second_intersection_point[2])/second_refracted_direction[2]
    x = second_intersection_point[0] + p*second_refracted_direction[0]
    y = second_intersection_point[1] + p*second_refracted_direction[1]

    all_x.append(x)
    all_z.append(second_intersection_point[2] + p*second_refracted_direction[2])  

    return (x, y, all_x, all_z)



angle_to_the_axis = np.arctan(400/1800)*rad_to_deg
#angle_to_the_axis = 0.
#angle_to_the_axis = 5.
#angle_to_the_axis = 10.
print("\n angle_to_the_axis in degrees: ", angle_to_the_axis)

sphere_center = np.array([0, 0, 1850.])
#print("\n sphere_center: ", sphere_center, "\n")

radius = 1900.  # in mm 
#print("\n radius: ", radius, "\n")

out_x = []
out_y = []
r_out = []

n = 16000


x, y, r_in, n = generate_points(n)

f3, ax3 = plt.subplots()
ax3.hist(r_in)
ax3.set_xlabel('r in [mm]', fontsize=20)
ax3.set_ylabel('count', fontsize=20)
plt.grid(True)
plt.show()

ax = plt.subplot()
for i in range(n):
    zz = find_z(np.array([x[i], y[i], -50]), angle_to_the_axis, sphere_center, radius)
    if zz is False:
        print("continue")
        continue
    out_x.append(zz[0])
    out_y.append(zz[1])
    r_out.append(np.sqrt(zz[0]*zz[0] + zz[1]*zz[1]))

    all_x = zz[2]
    all_z = zz[3]
    ax.plot(all_z, all_x)
ax.axis('equal')
ax.set_xlabel('z [mm]', fontsize=20)
ax.set_ylabel('x [mm]', fontsize=20)
plt.grid(True)
#f0, ax0 = plt.subplots()
#ax0.hist(out_x, bins=200)


#f1, ax1 = plt.subplots()
#ax1.hist(out_y, bins=200)

f1, ax1 = plt.subplots()
ax1.scatter(out_x, out_y)
ax1.axis('equal')
ax1.set_xlabel('x [mm]', fontsize=20)
ax1.set_ylabel('y [mm]', fontsize=20)
plt.grid(True)
plt.show()



f2, ax2 = plt.subplots()
ax2.hist(r_out)
ax2.set_xlabel('r out [mm]', fontsize=20)
ax2.set_ylabel('count', fontsize=20)
plt.grid(True)
plt.show()