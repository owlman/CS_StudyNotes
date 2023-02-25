#! /usr/bin/env python
'''
    Created on 2016-6-19
    
    @author: lingjie
    @name:   show_env_var
'''

import os
from check_platform import TestPlatform

TestPlatform()	

print ("--------System Environment Variables-----------------")
    
env_vars = os.environ
for item in env_vars.items():
	print( "[%s]: %s" % item)