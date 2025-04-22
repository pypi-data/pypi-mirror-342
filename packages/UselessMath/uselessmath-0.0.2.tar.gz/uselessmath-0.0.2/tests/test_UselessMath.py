import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UselessMath')))

import UselessMath

def test():
    assert UselessMath.Add(2, 2) == 4, "Add(2, 2) should be 4, test failed!"
    assert UselessMath.Add_One(2) == 3, "Add_One(2) should be 3, test failed!"
    assert UselessMath.Add_Zero(2) == 2, "Add_Zero(2) should be 2, test failed!"
    assert UselessMath.Division(2, 2) == 1, "Division(2, 2) should be 1, test failed!"
    assert UselessMath.Division(2, 0) == None, "Division(2, 0) should be None, test failed!"
    assert UselessMath.isEven(2) == True, "IsEven(2) should be True, test failed!"
    assert UselessMath.isOdd(2) == False, "IsOdd(2) should be False, test failed!"
    assert UselessMath.isNegative(-3) == True, "isNegative(-3) should be True, test failed!"
    assert UselessMath.isNotNegative(-3) == False, "isNotNegative(-3) should be False, test failed!"
    assert UselessMath.Multiplication(2, 2) == 4, "Multiplication(2, 2) should be 4, test failed!"
    assert UselessMath.One() == 1, "One() should be 1, test failed!"
    assert UselessMath.Opposite(1) == -1, "Opposite(1) should be 1, test failed!"
    assert UselessMath.Sqrt(4) == 2.0, "Sqrt(4) should be 2.0, test failed!"
    assert UselessMath.Sub(2,2) == 0, "Sub(2,2) should be 0, test failed!"
    assert UselessMath.WhatTheFuckIsThisNumber(42) == 42, "WhatTheFuckIsThisNumber(42) should be 42, test failed!"
    assert UselessMath.Zero() == 0, "Zero() should be 0, test failed!"

test()