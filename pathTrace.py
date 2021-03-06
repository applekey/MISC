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
    #print verts
    ## split by X
    if len(verts) == 1: # only 1 left, so value node
        print 'here'
        valueNode = kdTreeNode(-1,verts[0])
        leftRight(kdTree,goLeft,valueNode)
        return
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
            if vert[split] > med[split]:
                rightList.append(vert)
            else:
                leftList.append(vert)

        if len(rightList) == 0:
            ##add a new node for all of them
            kdTreeHelper(leftList,depth+1,splitNode,False)
        elif len(leftList) == 0:
            kdTreeHelper(rightList,depth+1,splitNode,True)
        else:
            kdTreeHelper(rightList,depth+1,splitNode,True)
            kdTreeHelper(leftList,depth+1,splitNode,False)
        return

def kdTree(verts):
    tree = kdHeadNode()

    kdTreeHelper(verts,0,tree,True)
    return tree

def verifyTree(tree):
    lft = tree.left
    right = tree.right
    count = 0
    if lft == None and right == None:
        if isinstance(tree.value, list):
            return len(tree.value)
        else:
            return 1
    else:

        if lft != None:
            count += verifyTree(lft)
        if right != None:
            count += verifyTree(right)
        return count




class ray():
    def __init__(self,position,direction):
        pass

def rayBouncer(x):
    pass

def drawImage(kdT,screenX,screenY,transform):
    ## spawn ortho rays for now
    map(lambda x: rayBouncer(x),range(screenX*screenY))

def main():
    faces = loadOBJ('/Users/applekey/Documents/obj/box.obj')
    print faces
    #create kd tree
    #print len(faces)
    #kdt = kdTree(faces)
    #print verifyTree(kdt)

main()
