"""
Author: Kevin Owens
Date: 12 May 2014
Class: LongCalc

Problem description summary (from TopCoder Tournament Inv 2001 Semi C+D 1000):  Do big-int math with two integer
operands and a an operator identifier for add, subtract, multiply, and integer divide.  Operands are given as strings;
operator is given as a numeric id 1:+, 2:-, 3:*, 4://.

Python makes this trivial.  Perhaps this 1000-point problem is geared toward other languages that don't natively
support arbitrarily large numbers?
"""

class LongCalc:

    def process(self, a_str, b_str, op):

        a = int(a_str)
        b = int(b_str)
        result = '#ERROR'

        if op == 1:  # addition

            result = str(a + b)

        elif op == 2:  # subtraction

            result = str(a - b)

        elif op == 3:  # multiplication

            result = str(a * b)

        elif op == 4:  # integer division

            result = str(a // b)

        return result


if __name__ == '__main__':

    lc = LongCalc()

    print(lc.process("100", "50", 1))  # "150"
    print(lc.process("100000000000000000000000000000000", "400000000000000000000000000000000", 1))
        # 500000000000000000000000000000000
    print(lc.process("3", "4", 2))  # "-1"
    print(lc.process("29", "465", 3))  # "13485"
    print(lc.process("15", "2", 4))  # "7"
