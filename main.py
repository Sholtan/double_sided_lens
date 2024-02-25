#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from .my_functions import get_intersection_point, reflect, rad_to_deg, deg_to_rad



def find_z(start_point, angle_to_the_axis, sphere_center, radius):
    all_x = []
    all_z = []

    all_x.append(start_point[0])
    all_z.append(start_point[2])


    direction = np.array([np.sin(angle_to_the_axis*deg_to_rad), 0, np.cos(angle_to_the_axis*deg_to_rad)])
    #print("\n direction: ", direction)

    intersection_point = get_intersection_point(start_point, direction, sphere_center, radius)
    #print("\n intersection_point: ", intersection_point)

    all_x.append(intersection_point[0])
    all_z.append(intersection_point[2])

    refracted_direction = reflect(direction, sphere_center, intersection_point, in_or_out='in')
    #print("\n refracted_direction: ", refracted_direction)

    second_intersection_point = get_intersection_point(intersection_point, refracted_direction, np.array([0, 0, -1850.]), radius)
    #print("\n second_intersection_point: ", second_intersection_point)

    all_x.append(second_intersection_point[0])
    all_z.append(second_intersection_point[2])   

    second_refracted_direction = reflect(refracted_direction, np.array([0, 0, -1850.]), second_intersection_point, in_or_out='out')
    #print("\n second_refracted_direction: ", second_refracted_direction)

    focal_distance = 1923.
    #focal_distance = 1600.

    p = (focal_distance - second_intersection_point[2])/second_refracted_direction[2]
    x = second_intersection_point[0] + p*second_refracted_direction[0]
    y = second_intersection_point[1] + p*second_refracted_direction[1]

    all_x.append(x)
    all_z.append(second_intersection_point[2] + p*second_refracted_direction[2])  

    return (all_x, all_z)


start_point = np.array([410., 0., -100.])
#print("\nstart_point: ", start_point, "\n")

angle_to_the_axis = 0.
#print("\n angle_to_the_axis: ", angle_to_the_axis)

sphere_center = np.array([0, 0, 1850.])
#print("\n sphere_center: ", sphere_center, "\n")

radius = 1900.  # in mm 
#print("\n radius: ", radius, "\n")

out_x = []
out_y = []

n = 200
rng = np.random.default_rng()

angles = 2*np.pi * rng.random((n,))
rs = 410* rng.random((n,))

x = []
y = []

for i in range(n):
    x.append(rs[i] * np.cos(angles[i]))
    y.append(rs[i] * np.sin(angles[i]))


ax = plt.subplot()
for i in range(n):
    zz = find_z(np.array([x[i], y[i], -100]), angle_to_the_axis, sphere_center, radius)
    #out_x.append(zz[0])
    #out_y.append(zz[1])
    all_x = zz[0]
    all_z = zz[1]
    #print("all_x: ", all_x)
    #print("all_z: ", all_z)
    ax.plot(all_z, all_x)


#f0, ax0 = plt.subplots()
#ax0.hist(out_x, bins=200)


#f1, ax1 = plt.subplots()
#ax1.hist(out_y, bins=200)


#ax.scatter(out_x, out_y)




ax.axis('equal')
ax.set_xlabel('z [mm]', fontsize=20)
ax.set_ylabel('x [mm]', fontsize=20)
plt.show()
