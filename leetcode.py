class Solution(object):
    def divide(self, dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """
        if abs(divisor) > abs(dividend):
            return 0

        if divisor == dividend:
            return 1
        if divisor == 0:
            return sys.maxint
        if dividend == 0:
            return 0

        a = 1
        b = 1
        if dividend < 0:
            a = -1

        if divisor < 0:
            b = -1

        bothSameSign = False
        if (a == 1 and b == 1) or (a == -1 and b == -1):
            bothSameSign = True

        val = 0
        iterator = 0

        while True: #lOLOLOLOL
            val += abs(divisor)
            if val <= abs(dividend):
                iterator +=1
            else:
                break
        if bothSameSign:
            return iterator
        else:
            return -iterator

sol = Solution()
print sol.divide(-6,4)
