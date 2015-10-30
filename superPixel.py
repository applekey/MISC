
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def vecNorm(myvec):
    mag =  math.sqrt(math.pow(myvec[0],2) + math.pow(myvec[1],2))
    return [myvec[0]/mag,myvec[1]/mag]

def CreateSurface():
    #draw half a sphere
    points = []
    radius = 15.0
    granularity = 500

    anglePerSlice =  180.0/granularity

    for i in range(granularity):
        x = -math.cos(math.radians(i*anglePerSlice)) * radius
        y = math.sin(math.radians(i*anglePerSlice)) * radius
        points.append([x,y])

    return points

class ray:
    def __init__(self,origin,direction):
        self.origin = origin
        self.direction = direction

def findCorrectEdgeRay(edges,ray):
    #construct aabb for each edge
    aabb = []
    for edge in edges:
        minLeft = [min(edge[0][0],edge[1][0]), max(edge[0][1],edge[1][1])]
        maxTop = [max(edge[0][0],edge[1][0]), min(edge[0][1],edge[1][1])]


        ## check if the ray intersects the aabb
        bottomIntersection = (minLeft[1] - ray.origin[1]) / ray.direction[1] * ray.direction[0]
        topIntersection = (maxTop[1] - ray.origin[1]) / ray.direction[1] * ray.direction[0]

        if ((bottomIntersection > minLeft[0] and bottomIntersection < maxTop[0])
            or(topIntersection > minLeft[0] and topIntersection < maxTop[0])):

            # print ray.direction
            #print edge[0][0]
            return edge
    print 'not found'
    return None
def findCorrectEdge(edges,xIndex):
    #print xIndex
    found = False
    for edge in edges:
        if xIndex == max(edge[1][0],edge[0][0]) or xIndex == min(edge[1][0],edge[0][0]):
            found = True
            return edge
        if xIndex <max(edge[1][0],edge[0][0]) and xIndex>min(edge[1][0],edge[0][0]):
            found = True
            return edge
    #print xIndex
    print 'notfound'

def TraceSpecular(edges):
    samples = 1000
    start = -10.0
    end = 10.0
    colors = []
    lightPos = [3,30]
    ## camera stuff
    camPos = [0,25]
    camNear = 3
    camFov = 80.0
    for i in range(samples):
        angle = -camFov/2.0 + camFov/samples * float(i)
        direction = [math.sin(math.radians(angle)), - 1.0]
        #print vecNorm(direction)
        #print angle
        #create the ray
        sampleRay = ray(camPos,(direction))

        edge = findCorrectEdgeRay(edges,sampleRay)

        if edge == None:
            continue

        #find rayslope
        if sampleRay.direction[0] == 0.0:
            sampleRay.direction[0] =0.01

        #print edge[0][0]


        raySlope = sampleRay.direction[1]/sampleRay.direction[0]
        raym = sampleRay.origin[1] - raySlope* sampleRay.origin[0]
        #find segmentslope
        segSlope = (edge[1][1] - edge[0][1])/(edge[1][0] - edge[0][0])
        #print segSlope
        segm = edge[1][1] - segSlope* edge[1][0]

        #print raySlope - segSlope

        iceptX = (segm - raym)/(raySlope - segSlope)
        iceptY = raym + raySlope*iceptX

        slope = [(edge[1][0] - edge[0][0]),(edge[1][1] - edge[1][1])]
        normal = slope
        normal[0] = -normal[0]
        normal = vecNorm(normal)

        lightDir = [lightPos[0] - iceptX,lightPos[1] - iceptY]
        lightDir = vecNorm(lightDir)

        factor = max(-(lightDir[0] * normal[0] + lightDir[1] * normal[1]),0)
        colors.append(255.0 * factor)
    return colors


def TraceDiffuse(edges):
    samples = 1000
    start = -10.0
    end = 10.0
    colors = []
    lightPos = [20,15]

    for i in range(samples):
        xIndex = start + (end-start)/samples * i #+ random.uniform(0,0.3)
        edge = findCorrectEdge(edges,xIndex)
        ## calculate lambert
        if edge == None:
            continue
        pYpos =  edge[0][1] + (-edge[0][0] + xIndex)/(edge[1][0] - edge[0][0]) * (edge[1][1] - edge[0][1])
        slope = [(edge[0][1] - edge[1][1]),(edge[0][0] - edge[1][0])]
        normal = slope
        normal[0] = -normal[0]
        normalNormalize = math.sqrt(math.pow(normal[0],2) + math.pow(normal[1],2))
        normal[0] = normal[0]/normalNormalize
        normal[1] = normal[1]/normalNormalize
        #print normal
        lightDirNormalize = math.sqrt(math.pow((lightPos[0] - xIndex),2) + math.pow((lightPos[1] - pYpos),2))
        lightDir = [(lightPos[0] - xIndex)/lightDirNormalize,(lightPos[1] - pYpos)/lightDirNormalize]
        factor = max(lightDir[0] * normal[0] + lightDir[1] * normal[1],0)
        colors.append(255.0 * factor)
    return colors

def output(colors):
    lenColors = len(colors[0])
    height = 400
    blank_image = np.zeros((height,lenColors,1), np.uint8)

    for i in range(lenColors):
        color = 0
        #color = colors[0][i]
        for m in range(len(colors)):
            color +=colors[m][i]
        color = color /float(len(colors))
        for j in range(height):
            blank_image[j][i] = color

    # x = [i for i in range(lenColors)]
    # y = [blank_image[0][i] for i in range(lenColors)]
    # plt.scatter(x, y)
    # plt.show()
    cv2.imwrite('/Users/applekey/Desktop/c.png',blank_image)

    # cv2.imshow('image',blank_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def main():
    points  = CreateSurface()
    edges = []
    allColors = []
    ## create edges
    plen = len(points)
    print plen

    skip = 5
    for s in range(skip):
        for i in range(plen)[10+s::skip]:
            edges.append([points[i-skip],points[i]])
        print len(edges)

        # for edge in edges:
        #     print str(edge[0][0]) + ' ' + str(edge[1][0])

        colors = TraceSpecular(edges)
        allColors.append(colors)
        edges = []
    output(allColors)
main()
