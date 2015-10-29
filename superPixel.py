
import math
import cv2
import numpy as np
def CreateSurface():
    #draw half a sphere
    points = []
    radius = 10.0
    granularity = 500

    anglePerSlice =  180.0/granularity

    for i in range(granularity):
        x = math.cos(math.radians(i*anglePerSlice)) * radius
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

def Trace(edges):
    samples = 100
    start = -10.0
    end = 10.0
    colors = []
    lightPos = [5,15]

    for i in range(samples):
        xIndex = start + (end-start)/samples * i
        edge = findCorrectEdge(edges,xIndex)
        ## calculate lambert
            #interpolate y position
        if edge == None:
            continue
        pYpos =  edge[0][1] + (edge[0][0] - xIndex)/(edge[0][0] - edge[1][0]) * (edge[1][1] - edge[0][1])
        slope = [(edge[0][1] - edge[1][1]),(edge[0][0] - edge[1][0])]
        normal = slope
        normal[0] = -normal[0]
        #print normal
        lightDir = [(lightPos[0] - xIndex),(lightPos[1] - pYpos)]
        factor = max(lightDir[0] * normal[0] + lightDir[1] * normal[1],0)
        colors.append(255.0 * factor)
    return colors

def output(colors):
    lenColors = len(colors)
    blank_image = np.zeros((30,lenColors,1), np.uint8)
    cv2.show
def main():
    points  = CreateSurface()
    edges = []

    ## create edges
    plen = len(points)

    for i in range(plen)[1::]:
        edges.append([points[i-1],points[i]])

    colors = Trace(edges)

main()
