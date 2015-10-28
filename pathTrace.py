def findMed(verts,index):
    vertSorted = sorted(verts, key=lambda vert: vert[index])
    return vertSorted[len(vertSorted)/2]

def loadOBJ(filename):
    numVerts = 0
    verts = []
    norms = []
    vertsOut = []
    normsOut = []
    for line in open(filename, "r"):
        vals = line.split()
        if vals[0] == "v":
            v = map(float, vals[1:4])
            verts.append(v)
        if vals[0] == "vn":
            n = map(float, vals[1:4])
            norms.append(n)
        if vals[0] == "f":
            for f in vals[1:]:
                w = f.split("/")
                #OBJ Files are 1-indexed so we must subtract 1 below
                vertsOut.append(list(verts[int(w[0])-1]))
                #normsOut.append(list(norms[int(w[2])-1]))
                numVerts += 1
    return vertsOut


class kdHeadNode:
    def __init__(self):
        self.left = None
        self.right = None

class kdTreeNode:
    # -1 axis is leaf
    def __init__(self,axis,value):
        self.axis = axis
        self.value = value
        self.left = None
        self.right = None


def leftRight(node,lftRight,childNode):
    if lftRight:
        node.left = childNode
    else:
        node.right = childNode

## i j k indicies
def kdTreeHelper(verts,depth,kdTree,goLeft):
    split = depth % 3

    ## split by X
    if len(verts) == 1: # only 1 left, so value node
        valueNode = kdTreeNode(-1,verts[splitStartIndex])
        leftRight(kdTree,goLeft,valueNode)
    else:
        ## split
        # create a node to represent the split
        med = findMed(verts, split )


        splitNode = kdTreeNode(split,med[split])
        leftRight(kdTree,goLeft,splitNode)
        ## find the median


        rightList = []
        leftList = []
        for vert in verts:
            if vert[split] > med:
                rightList.append(vert)
            else:
                leftList.append(vert)

        kdTreeHelper(rightList,depth+1,splitNode,True)
        kdTreeHelper(leftList,depth+1,splitNode,False)


def kdTree(verts):
    tree = kdHeadNode()

    kdTreeHelper(verts,0,tree,True)
    return tree


faces = loadOBJ('/Users/applekey/Documents/obj/sphere.obj')
#create kd tree
kdT = kdTree(faces)

#swap rays

class ray():
    def __init__(self,position,direction):
        pass

def rayBouncer(x):
    pass

def drawImage(kdT,screenX,screenY,transform):
    ## spawn ortho rays for now
    map(lambda x: rayBouncer(x),range(screenX*screenY))
