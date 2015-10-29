
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

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
    lightPos = [10,15]
    for i in range(samples):
        xIndex = start + (end-start)/samples * i + random.uniform(0,0.3)
        edge = findCorrectEdge(edges,xIndex)

        if edge == None:
            continue
        pYpos =  edge[0][1] + (-edge[0][0] + xIndex)/(edge[1][0] - edge[0][0]) * (edge[1][1] - edge[0][1])
        slope = [(edge[0][1] - edge[1][1]),(edge[0][0] - edge[1][0])]
        normal = slope
        normal[0] = -normal[0]




def TraceDiffuse(edges):
    samples = 1000
    start = -10.0
    end = 10.0
    colors = []
    lightPos = [10,15]

    for i in range(samples):
        xIndex = start + (end-start)/samples * i + random.uniform(0,0.3)
        edge = findCorrectEdge(edges,xIndex)
        ## calculate lambert
            #interpolate y position
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

    x = [i for i in range(lenColors)]
    y = [blank_image[0][i] for i in range(lenColors)]
    plt.scatter(x, y)
    plt.show()
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
    skip = 6
    for s in range(skip):
        for i in range(plen)[10+s::skip]:
            edges.append([points[i-skip],points[i]])
        print len(edges)

        # for edge in edges:
        #     print str(edge[0][0]) + ' ' + str(edge[1][0])

        colors = TraceDiffuse(edges)
        allColors.append(colors)
        edges = []
    output(allColors)
main()
