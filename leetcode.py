class NumArray(object):
    def myLevelConstructor(self, values, indexes, currentWorkingCount):
        if currentWorkingCount <2:
            return

        ## startAtEndOf 0, 8, prev index -2

        workingIndex = indexes[-2]
        workingIndex +=1
        newElementsAdded = 0
        while workingIndex < indexes[-1]:
            values.append(values[workingIndex-1] + values[workingIndex])
            workingIndex += 2
            newElementsAdded += 1

        if workingIndex == indexes[-1]:
            values.append(values[workingIndex - 1])
            newElementsAdded +=1
        indexes.append(indexes[-1] + newElementsAdded)
        self.myLevelConstructor(values,indexes, newElementsAdded)

    def __init__(self, nums):
        """
            initialize your data structure here.
            :type nums: List[int]
            """
        self.values = []
        for num in nums:
            self.values.append(num)
        self.indexes = [0,len(nums)] ## index tracker
        self.myLevelConstructor(self.values,self.indexes,len(nums))


    def update(self, i, val):
        difference = val - self.values[i]
        division = 1
        for k in range(1, len(self.indexes)):
            index =  i / division + self.indexes[k-1]
            self.values[index] += difference
            division *= 2

    def sumRange(self, i, j):
        if i < 0:
            return 0
        if j >= self.indexes[1]:
            return 0
        # go right
        sum = 0
        left = i

        while left <= j:
            divisor = 2
            levels = 0
            currentIndex = left
            canGoRight = True
            while canGoRight:
                if left % divisor == 0 and currentIndex <= j:
                    divisor *=2
                    levels += 1
                else:
                    canGoRight = False
                    lvlIndex = self.indexes[levels] + left / pow(2,levels)
                    print lvlIndex
                    sum += self.values[lvlIndex]
                #print levels
                currentIndex = left + pow(2,levels)
                #print currentIndex

            left = currentIndex
        print sum

    def printTree(self):
        for k in range(len(self.indexes)-1):
            for i in range(self.indexes[k],self.indexes[k+1]):
                print self.values[i],
            print '\n'



nums = [1,2,3,4,5,6,7,8]
numAr = NumArray(nums)
# numAr.printTree()
#numAr.update(0,3)
# numAr.printTree()
numAr.sumRange(0,2)




#pos[0].xy = pos[0].xy + pl*( (e2.xy/dot(e2.xy,n0.xy)) + (e0.xy/dot(e0.xy,n2.xy)) );
#    pos[1].xy = pos[1].xy + pl*( (e0.xy/dot(e0.xy,n1.xy)) + (e1.xy/dot(e1.xy,n0.xy)) );
#    pos[2].xy = pos[2].xy + pl*( (e1.xy/dot(e1.xy,n2.xy)) + (e2.xy/dot(e2.xy,n1.xy)) );
#
#class TreeNode(object):
#    def __init__(self, x):
#        self.val = x
#        self.left = None
#        self.right = None
#
#class Solution(object):
#    def maxPathSum(self, root):
#        """
#        :type root: TreeNode
#        :rtype: int
#        """

# class Solution(object):
#     def largestRectangleArea(self, height):
#         """
#         :type height: List[int]
#         :rtype: int
#         """
#         biggestArea = -1
#         hstack = [(-9999,0)]
#         for index, h in enumerate(height):
#             if h > hstack[-1][0]: #push onto stack
#                 hstack.append((h,index))
#                 if h > biggestArea:
#                     biggestArea = h
#
#             elif h == hstack[-1][0]:
#                 nth = hstack[-1][1]+1
#                 hstack.append((h,nth))
#                 newArea = h * nth
#                 if newArea > biggestArea:
#                     biggestArea = newArea
#
#             else: # new to deque until we find the right one
#                 while hstack[-1][0] > h and len(hstack) > 0:
#                     hstack.pop(1)
#                 # find the prev
#                 if len(hstack) > 0:
#                     prev
#                 else:
#                     hstack.append((h,index))
#                     if h > biggestArea:
#                         biggestArea = h
#
#         return biggestArea
#
# a = Solution()
# a.largestRectangleArea([2,1,5,6,2,3])

# class Solution(object):
#     def reverseWords(self, s):
#         """
#         :type s: str
#         :rtype: str
#         """
#         rtr = ''
#         for word in reversed(s.split()):
#             rtr += word + ' '
#         return rtr[:-1:]
#
# a = Solution()
# print a.reverseWords('  a   b  ')
# #Contains Duplicate III
# class Solution(object):
#     def containsNearbyAlmostDuplicate(self, nums, k, t):
#         """
#         :type nums: List[int]
#         :type k: int
#         :type t: int
#         :rtype: bool
#        """


# # Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None
#
# class Solution(object):
#     def Slice(self, prev,sliceElement):
#         tmp = prev.next
#         prev.next = sliceElement
#         sliceElement.next = tmp
#
#     def printList(self,lia):
#         while lia!= None:
#             print lia.val
#             lia = lia.next
#
#     def reorderList(self, head):
#         """
#         :type head: ListNode
#         :rtype: void Do not return anything, modify head in-place instead.
#         """
#         if head == None or head.next == None:
#             return
#
#
#         ## check if its even or odd
#         frontHead = head
#         curPtr = head.next
#         prev = head
#         count = 0
#
#         while True:
#             count += 1
#             prev = curPtr
#             curPtr = curPtr.next
#
#             if curPtr == None:
#                 break
#             else:
#                 curPtr.prev = prev
#
#         #self.printList(frontHead)
#         half = count /2
#         currentBack = prev ## this is the last pointer
#
#         for i in range(half):
#             nxtPtr = frontHead.next
#             self.Slice(frontHead,currentBack)
#             currentBack = currentBack.prev
#             frontHead = nxtPtr
#
#         if count %2 == 0:
#             frontHead.next = None
#         else:
#             frontHead.next.next = None
#
#
# a = ListNode(1)
# b = ListNode(2)
# c = ListNode(3)
# d = ListNode(4)
# e = ListNode(5)
# f = ListNode(6)

# a.next = b
# b.next = c
# c.next = d
# d.next = e
# e.next = f


# aa = Solution()
# aa.reorderList(a)
# aa.printList(a)

# abc = [3,5,6,2,5,4,19,5,6,7,12]
# class Solution(object):
#     def lengthOfLIS(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: int
#         """
#         lists = []
#
#         if len(nums) == 0:
#             return 0
#
#         for num in nums:
#             print lists
#             if len(lists) == 0: #case 1
#                 lists.append([num])
#             elif num > lists[-1][-1]: # case 2 ,clone and append
#                 prev = lists[-1]
#                 newList = prev[:]
#                 newList.append(num)
#                 lists.append(newList)
#             else: #potential case 3 , check previous
#                 for alist in (lists):
#                     if num < alist[-1]:
#                         if len(alist) >1:
#                             if alist[-2] == num:
#                                 break;
#
#                         alist[-1] = num
#                         break;
#         return len(lists[-1])
# a = Solution()
# print  a.lengthOfLIS(abc)




# class Solution(object):
#     def maximalSquare(self, matrix):
#         """
#         :type matrix: List[List[str]]
#         :rtype: int
#         """
#         if len(matrix) == 0:
#             return 0
#
#
#         counts = [0] * len(matrix[0])
#         largest = 0
#         for row in matrix:
#             listToCheck = []
#             for index,col in enumerate(list(row)):
#                 if col == '1':
#                     if largest == 0:
#                         largest = 1
#
#                     currentHeight =  counts[index] +1
#                     counts[index] = currentHeight
#
#
#
#                     needed = currentHeight -12
#                     #print 'abc' +str(listToCheck) + 'sfda ' + str(needed)
#                     for prev in reversed(listToCheck):
#                         #if same height
#                         if prev >= currentHeight:
#                             needed -= 1
#                             if needed == 0:
#                                 break;
#                         else:
#                             needed -= currentHeight - prev
#                             currentHeight = prev
#                             needed -= 1
#                             if needed <= 0:
#                                 break;
#
#                     if needed <= 0:
#                         if currentHeight > largest:
#                             largest = currentHeight
#
#                     listToCheck.append(counts[index])
#                 else:
#                     listToCheck = []
#                     counts[index] = 0
#             #print counts
#         return largest * largest
# a = Solution()
# mat = ["0001010","0100000","0101001","0011001","1111110","1001011","0100101","1101110","1010101","1110000"]
# print a.maximalSquare(mat)

# class Solution(object):
#     def threeSum(self, nums):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         mList = []
#         lenList = len(nums)
#         answers = []
#
#         for i in range(lenList):
#             target = -nums[i]
#             for j in range(i+1,lenList):
#                 numj = nums[j]
#                 difference = target - numj
#                 if difference in mList:
#                     ans = sorted([-target,numj,difference])
#                     if ans not in answers:
#                         answers.append(ans)
#                 # not found, keep searching
#                 else:
#                     mList.append(numj)
#         return answers
#
# a = Solution()
# inputs = [-1,0,3,4,5,1,-3]
# input = [-7,-10,-1,3,0,-7,-9,-1,10,8,-6,4,14,-8,9,-15,0,-4,-5,9,11,3,-5,-8,2,-6,-14,7,-14,10,5,-6,7,11,4,-7,11,11,7,7,-4,-14,-12,-13,-14,4,-13,1,-15,-2,-12,11,-14,-2,10,3,-1,11,-5,1,-2,7,2,-10,-5,-8,-10,14,10,13,-2,-9,6,-7,-7,7,12,-5,-14,4,0,-11,-8,2,-6,-13,12,0,5,-15,8,-12,-1,-4,-15,2,-5,-9,-7,12,11,6,10,-6,14,-12,9,3,-10,10,-8,-2,6,-9,7,7,-7,4,-8,5,-4,8,0,3,11,0,-10,-9]
# print a.threeSum(input)

# class Solution(object):
#
#     def threeSum(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: List[List[int]]
#         """
#
#         nums = sorted(nums)
#         totalLength = len(nums)
#
#         result =[]
#
#         for i in range(totalLength):
#             if nums[i] > 0:
#                 break
#             for j in range(i+1,totalLength):
#
#                 secondSum = nums[i] + nums[j]
#
#                 if secondSum > 0:
#                     break;
#
#                 diffToZero = 0 - secondSum
#
#                 if nums[j] > diffToZero:
#                     break
#
#                 for k in range(j+1,totalLength):
#                     thirdSum = nums[i] + nums[j] + nums[k]
#
#                     if thirdSum == 0:
#                         newval = [nums[i],nums[j],nums[k]]
#                         if not newval in result:
#                             result.append(newval)
#
#         return result
#
# a = Solution()
# input = [8,5,12,3,-2,-13,-8,-9,-8,10,-10,-10,-14,-5,-1,-8,-7,-12,4,4,10,-8,0,-3,4,11,-9,-2,-7,-2,3,-14,-12,1,-4,-6,3,3,0,2,-9,-2,7,-8,0,14,-1,8,-13,10,-11,4,-13,-4,-14,-1,-8,-7,12,-8,6,0,-15,2,8,-4,11,-4,-15,-12,5,-9,1,-2,-10,-14,-11,4,1,13,-1,-3,3,-7,9,-4,7,8,4,4,8,-12,12,8,5,5,12,-7,9,4,-12,-1,2,5,4,7,-2,8,-12,-15,-1,2,-11]
# print a.threeSum(input)

# class Solution(object):
#     def recMidSearch(self,lista,listb,i,iend,j,jend,kthSmallest,firstTime,moveA):
#
#         ## larger  always has to conform to the smaller
#
#          if i ==  z
#
#
#         if firstTime:
#             ## find the smallest
#
#         imid = (i + iend) / 2
#         jmid = (j + jend) / 2
#
#         if lista[imid] < listb[jmid]:
#             return self.recMidSearch(lista,listb,imid,iend,j,jmid,kthSmallest,False,moveA)
#         else:
#             return self.recMidSearch(lista,listb,i,imid,jmid,jend,kthSmallest,False,moveA)
#
#     def findMedianSortedArrays(self, nums1, nums2,smallest):
#         """
#         :type nums1: List[int]
#         :type nums2: List[int]
#         :rtype: float
#         """
#         moveA = True if len(nums1) < len(nums2) else False
#
#         return self.recMidSearch(nums1,nums2,0,len(nums1) -1,0,len(nums2) - 1,smallest,True,moveA)
#
# ## need to find the ith elemnt
#
# nums1 = [0, 2,4,6]
# nums2 = [-1,1,3,5,7,9]
# a = Solution()
# print a.findMedianSortedArrays(nums1,nums2,1)

# class Solution(object):
#     def nxtMoves(self,s,AorB):
#         moves = self.generatePossibleNextMoves(s)
#         if len(moves) == 0:
#             if AorB: ## its A's turn and there are no more moves
#                 return 1
#             else:
#                 return 0 ## a wins
#         ans = map(lambda x:self.nxtMoves(x,not AorB),moves)
#         return reduce(lambda x,y:x+y,ans)
#
#     def generatePossibleNextMoves(self, s):
#         """
#         :type s: str
#         :rtype: List[str]
#         """
#         ans = []
#         if len(s) < 2:
#             return ans
#         for idx,val in enumerate(s[1:]):
#             ridx = idx+1
#             if val == s[ridx-1] and val == '+':
#                 cpy = s[:ridx-1] +"--"+ s[ridx+1:]
#                 ans.append(cpy)
#         return ans
#     def canWin(self, s):
#         """
#         :type s: str
#         :rtype: bool
#         """
#         if s == "":
#             return False
#         moves = self.generatePossibleNextMoves(s)
#
#         if len(moves) == 0:
#             return False
#
#         ans = map(lambda x:self.nxtMoves(x,False),moves)
#
#         willWork = False
#         for a in ans:
#             if a == 0:
#                 willWork = True
#                 break
#         return willWork
#
# input = "++++++-++++++-++++++"
# a = Solution()
# print a.canWin(input)
# class Solution(object):
#     def generatePossibleNextMoves(self, s):
#         """
#         :type s: str
#         :rtype: List[str]
#         """
#         ans = []
#         if len(s) < 2:
#             return ans
#
#         for idx,val in enumerate(s[1:]):
#             ridx = idx+1
#             if val == s[ridx-1] and val == '+':
#                 cpy = s[:ridx-1] +"--"+ s[ridx+1:]
#                 ans.append(cpy)
#         return ans
#
# ####
# input = '++++'
# a = Solution()
# print a.generatePossibleNextMoves(input)

# class Solution(object):
#     def merge(self,lista,listb):
#         sol = []
#         a = lista
#         b = listb
#         lenListA = len(lista)
#         lenListB = len(listb)
#         while lenListA > 0 or lenListB > 0:
#             if lenListB == 0:
#                 sol = sol + a
#                 break
#             if lenListA == 0:
#                 sol = sol + b
#                 break
#
#             if a[0][0] < b[0][0]:
#                 sol.append(a[0])
#                 a = a[1:]
#                 lenListA -=1
#             else:
#                 sol.append(b[0])
#                 b = b[1:]
#                 lenListB -=1
#
#         return sol
#
#
#         if lista[0] < listb:
#             sol.append(lista[0])
#     def getSkyline(self, buildings):
#         """
#         :type buildings: List[List[int]]
#         :rtype: List[List[int]]
#         """
#         if len(buildings) == 0:
#             return buildings
#
#         result = []
#
#         segments = [[-2,-1,[]]]
#         end = -1
#         for building in buildings:
#             if building[0] > end:
#                 # current segment has ended
#                 segments.append([building[0],building[1],[building]])
#                 # add myself to a new segment
#                 end  = building[1]
#                 #set end to me
#             else:
#                 if building[1] > end:
#                     # i am within current segment, but longer than it
#                     end = building[1]
#                     segments[-1][1] = end
#                     #add myself to the current segment
#                     segments[-1][2].append(building)
#                 else:
#                     # iam within current segment, and contained within it
#                     segments[-1][2].append(building)
#         segments = segments[1:]
#         for segment in segments:
#             #sort based on height
#             blocks = segment[2]
#             #sortedBlocks = sorted(blocks,key=lambda blocks: blocks[2],reverse=True)
#             #print blocks
#
#             starts = map(lambda x:(x[0],x[2]),blocks)
#
#             ends = map(lambda x:(x[1],str(x[2])+'*'),blocks)
#             #print ends
#             ends = sorted(ends, key = lambda x:x[0])
#             rails= self.merge(starts,ends)
#             #print rails
#             heights = [-1]
#             points = []
#             for rai in rails:
#                 #$print heights
#                 #check if we are beginning or end block
#                 if type(rai[1]) is str: # this is end block
#                     # get the endHeight
#                     endHeight  = int(rai[1][:-1])
#                     #print endHeight
#                     if endHeight == heights[-1]:
#                         secondHeight = heights[-2]
#                         if secondHeight == -1:
#                             secondHeight = 0
#                         points.append([rai[0],secondHeight])
#                     heights.remove(endHeight)
#                 else:
#                     # this is startBlock
#                     #if the block height is larger than active top, then add it
#                     lftHeight = rai[1]
#
#                     if lftHeight > heights[-1]:
#                         heights.append(lftHeight)
#                         points.append([rai[0],lftHeight])
#                     else:
#                         heights.append(lftHeight)
#                     heights.sort()
#             result += points
#         return result
#
#
#
#
#         #print segments
#
#
#
# sol = Solution();
#
# input = [ [2 ,9 ,10], [3, 7 ,15], [5, 12 ,12], [15 ,20, 10], [19, 24 ,8] ]
# print sol.getSkyline(input)
#
#


# class Solution(object):
#     def divisorFind(self, dividend, divisor,left,right):
#         #print left,right, dividend
#         if left == right:
#             if (divisor << left) < dividend:
#                 #print 'a'
#                 return left, False
#             elif (divisor << left) == dividend:
#                 #print 'b'
#                 return left, True
#             else:
#                 #print 'c'
#                 return left -1 ,False
#
#         shiftMid = (left + right) / 2
#         shiftedVal = divisor << shiftMid
#
#         if dividend < shiftedVal: # go left
#             if left == shiftMid:
#                 return self.divisorFind(dividend,divisor,left,shiftMid)
#             else:
#                 return self.divisorFind(dividend,divisor,left,shiftMid - 1)
#         elif dividend == shiftedVal:
#             return shiftMid,True
#         else: # go right
#             return self.divisorFind(dividend,divisor,shiftMid + 1,right)
#
#     def divide(self, dividend, divisor):
#         """
#         :type dividend: int
#         :type divisor: int
#         :rtype: int
#         """
#
#         if divisor == dividend:
#             return 1
#         if divisor == 0:
#             return sys.maxint
#         if dividend == 0:
#             return 0
#
#         if divisor == 1:
#             return dividend
#         if divisor == -1:
#             return -dividend
#
#         if dividend == -2147483648:
#             if divisor <0:
#                 dividend = -2147483647
#
#
#
#         if abs(divisor) > abs(dividend):
#             return 0
#
#
#
#         a = 1
#         b = 1
#
#
#         bothSameSign = False
#         if (divisor >0 and dividend > 0) or (divisor < 0 and dividend < 0):
#             bothSameSign = True
#
#         iterator = []
#
#         divisorAddition = abs(divisor)
#
#         divisorAbs = abs(divisor)
#         dividendAbs = abs(dividend)
#
#         while True: #lOLOLOLOL
#             (shifts, found) = self.divisorFind(dividendAbs,divisorAbs,0,31)
#             if shifts< 0:
#                 break;
#
#             if found or shifts == 0:
#                 iterator.append( shifts )
#                 break;
#             else:
#                 #print -99,dividend, divisor<<shifts
#                 #print shifts,dividendAbs,divisorAbs<<shifts
#                 dividendAbs = dividendAbs - (divisorAbs<<shifts)
#                 print dividendAbs
#                 iterator.append(shifts)
#         #print iterator
#         #print bothSameSign
#         ans = 0
#         for i in iterator:
#             ans += 1<<i
#         #iterator +=1
#         if bothSameSign:
#             return ans
#         else:
#             return -ans
#
# sol = Solution()
# print sol.divide(-2147483648,2)
