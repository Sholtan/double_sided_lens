#!/usr/bin/env python3

import numpy as np

refractive_index = {'air':1.0, 'lens':1.5025}
rad_to_deg = 180./np.pi
deg_to_rad = np.pi/180

def get_intersection_point(start_point, direction, sphere_center, radius):
    a = 1
    b = 2*np.sum(direction*(start_point - sphere_center))
    c = np.sum((start_point - sphere_center)*(start_point - sphere_center)) - radius*radius

    discriminant = b*b - 4*a*c

    p1 = (-b + np.sqrt(discriminant)) / (2 * a)
    p2 = (-b - np.sqrt(discriminant)) / (2 * a)

    #print("(p1, p2): ", (p1, p2))

    if p1<0 and p2<0:
        raise Exception('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! sphere is behind the photon, no intercection')
    elif p1<0:
        p = p2
        #print("\n p: ", p)
    elif p2<0:
        p = p1
        #print("\n p: ", p)
    elif p1 < p2:
        p = p1
        #print("\n p: ", p)
    else:
        p = p2
        #print("\n p: ", p)
    #print("start_point, p, direction", (start_point, p, direction), "\n\n")
    point = np.array(start_point + p * direction)
    distance_from_axis = np.sqrt(point[0]*point[0] + point[1]*point[1])
    if distance_from_axis > 410:
        raise Exception('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Intersection point is too far from axis')
    return point


def reflect(direction, sphere_center, intersection_point, in_or_out):
    if in_or_out=='in':
        normal = -intersection_point + sphere_center
    elif in_or_out=='out':
        normal = intersection_point - sphere_center
    else:
        raise Exception('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! photon shoud be going In or Out, check function arguments!\n')

    #print(" # normal: ", normal)
    normal = normal/np.linalg.norm(normal)
    #print(" # normal: ", normal)
    #print("np.linalg.norm(normal): ", np.linalg.norm(normal))

    alpha = np.arccos(np.sum(direction*normal))
    #print("alpha in deg = ", alpha*rad_to_deg)

    if alpha*rad_to_deg>90.:
        raise Exception('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! incident angle is more than 90 degrees!\n')

    if np.abs(alpha-np.pi)<1e-7 or alpha<1e-7:
        print()
        print("alpha-np.pi: ", alpha-np.pi)
        print("this particular photon went at straight right angle to the surface, what a coincidence!")
        return direction

    if in_or_out=='in':
        betta = np.arcsin(refractive_index['air']*np.sin(alpha)/refractive_index['lens'])
        #print("betta in deg: ", betta*rad_to_deg)
    elif in_or_out=='out':
        betta = np.arcsin(refractive_index['lens']*np.sin(alpha)/refractive_index['air'])
        #print("betta in deg: ", betta*rad_to_deg)
    else:
        raise Exception('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! photon shoud be going In or Out, check function arguments!\n')

    new_z = normal
    new_x = direction - np.dot(normal, direction)*normal
    new_x = new_x/np.linalg.norm(new_x)
    #print("\nnew_x: ", new_x)
    #print("\nnew_x*new_z: ", np.dot(new_x, new_z))
    new_y = np.cross(new_z, new_x)
    #print("new_y: ", new_y)

    first_intersection_inverse_matrix = np.stack((new_x, new_y, normal), axis=-1)
    first_intersection_matrix = np.linalg.inv(first_intersection_inverse_matrix)
    #print("\nfirst_intersection_inverse_matrix: ", first_intersection_inverse_matrix)
    #print("\nfirst_intersection_matrix: ", first_intersection_matrix)
    #print("\n matrix*itsInverse: ", np.dot(first_intersection_matrix, first_intersection_matrix))


    direction_SCS = np.array([np.sin(alpha), 0, np.cos(alpha)])
    #print("\n #### direction_SCS: ", direction_SCS)
    #print("\ndirection: ", direction)

    #print("\ninv_matrix*dir_SCS: ", np.dot(first_intersection_inverse_matrix, direction_SCS))
    #print("\n #### matrix*dir: ", np.dot(first_intersection_matrix, direction))

    refracted_direction = np.array([np.sin(betta), 0, np.cos(betta)])
    #print("\n #### refracted_direction", refracted_direction)
    refracted_direction = np.dot(first_intersection_inverse_matrix, refracted_direction)

    #print("\n refracted_direction", refracted_direction)

    return refracted_direction



