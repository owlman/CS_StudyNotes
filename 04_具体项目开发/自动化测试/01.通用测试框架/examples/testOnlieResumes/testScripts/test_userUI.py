import pytest

@pytest.mark.run(order=2)
def testfunc(): 
    print("userUI")