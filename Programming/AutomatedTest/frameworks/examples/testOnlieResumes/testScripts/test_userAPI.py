import pytest

@pytest.mark.run(order=3)
def testfunc(): 
    print("userAPI")