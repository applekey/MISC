class Solution(object):
    def recMidSearch(self,lista,listb,kthSmallest,firstTime):
        print lista
        print listb
        lenA = len(lista)
        lenB = len(listb)

        if firstTime:
            totalLength = lenA + lenB

            if totalLength < kthSmallest +1:
                print 'toolong ... thats what she said'
                return

            if kthSmallest == 0:
                return lista[0] if lista[0]< listb[1] else listb[1]
            if lenA < kthSmallest+1:
                ka = lenA-1
                kb = kthSmallest-ka -1
                print 'fdsa'
                print ka
                print kb
            else:
                ka = kthSmallest/2
                kb = kthSmallest - ka -1
                print ka
                print kb
        else:
            ka = lenA/2 -1
            kb = lenB/2 -1


        ## figure out that shit...
        if lenA == lenB and lenA == 1:
            ## which one do i return
            return lista[0]
        if lenA == 1 or lenB == 1:
            return lista[-1] if lista[-1]> listb[-1] else listb[-1]
            #return  lista

        # k/2 elemnt for both
        if lista[ka] < listb[kb]:
            #....axxx
            #xxxxb....
            return self.recMidSearch(lista[ka:kthSmallest+1],listb[:kb+1],kthSmallest,False)
        else:
            return self.recMidSearch(lista[:ka+1],listb[kb:kthSmallest+1],kthSmallest,False)

    def findMedianSortedArrays(self, nums1, nums2,smallest):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        return self.recMidSearch(nums1,nums2,smallest,True)

## need to find the ith elemnt

nums1 = [0, 1,2,3]
nums2 = [4,5,6,7,8,9]
a = Solution()
print a.findMedianSortedArrays(nums1,nums2,1)

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
