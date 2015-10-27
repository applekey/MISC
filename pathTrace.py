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
    def __init__(self,bounds):
        self.bounds = bounds
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
def kdTreeHelper(xVerts,yVerts,zVerts,i,iend,j,jend,k,kend,depth,kdTree,goLeft):
    split = depth % 3

    splitStartIndex = -1
    splitStartEndIndex = -1
    triList = None
    verts = []
    if split == 0:
        splitStartIndex = i
        splitStartEndIndex = iend
        triList = xVerts
    if split == 1:
        splitStartIndex = j
        splitStartEndIndex = jend
        triList = yVerts
    if split == 2:
        splitStartIndex = k
        splitStartEndIndex = kend
        triList = zVerts

    ## split by X
    if splitStartIndex == splitStartEndIndex: # only 1 left, so value node
        valueNode = kdTreeNode(-1,triList[i])
        leftRight(kdTree,goLeft,valueNode)
    else:
        ## split
        # create a node to represent the split

        mid = (i+j)/2
        splitA = kdTreeNode(split,mid)
        leftRight(kdTree,goLeft,splitA)

        kdTreeHelper(xVerts,yVerts,zVerts,i,mid,j,jend,k,kend,depth+1,splitA,True)
        kdTreeHelper(xVerts,yVerts,zVerts,mid+1,iend,j,jend,k,kend,depth+1,splitA,False)

def kdTree(verts):
#split depth
    depth = 4
    #

    sortedX = sorted(verts, key=lambda vert: vert[0])
    sortedY = sorted(verts, key=lambda vert: vert[1])
    sortedZ = sorted(verts, key=lambda vert: vert[2])

    bounds = [sortedX[0],sortedX[-1],sortedY[0],sortedY[-1],sortedZ[0],sortedZ[-1]]
    tree = kdHeadNode(bounds)

    margs = [sortedX,sortedY,sortedZ,0,len(sortedX),0,len(sortedY),0,len(sortedZ),0, tree, True]
    print len(margs)
    start = True
    kdTreeHelper(*margs)
    return tree


faces = loadOBJ('/Users/applekey/Documents/obj/bunny.obj')
#print faces

kdTree(faces)
