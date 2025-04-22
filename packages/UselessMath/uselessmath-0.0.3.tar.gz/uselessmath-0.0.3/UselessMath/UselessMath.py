import math

def isOdd(num):
    if num%2 != 0:
        return True
    else:
        return False

def isEven(num):
    if num%2 == 0:
        return True
    else:
        return False

def Sqrt(num):
    try:
        sqrt_num = math.sqrt(num)
    except ValueError:
        sqrt_num = None
    return sqrt_num

def Opposite(num):
    return -num

def Add_Zero(num):
    return num+0

def Add_One(num):
    return num+1

def Add(num1, num2):
    try:
        return num1+num2
    except ValueError:
        return None

def Sub(num1, num2):
    try:
        return num1-num2
    except ValueError:
        return None

def Multiplication(num1, num2):
    try:
        return num1*num2
    except ValueError:
        return None

def Division(num1, num2):
    if num2 == 0:
        return None
    else:
        try:
            return num1/num2
        except ValueError:
            return None

def isNegative(num):
    if "-" in str(num):
        return True
    else:
        return False
    
def isNotNegative(num):
    if not "-" in str(num):
        return True
    else:
        return False

def Zero():
    return 0

def One():
    return 1

def WhatTheFuckIsThisNumber(num):
    return num