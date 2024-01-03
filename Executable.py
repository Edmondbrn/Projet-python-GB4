import os
os.chdir(os.path.join(os.path.dirname(__file__), "Script"))
print(os.getcwd())

from Script.application import *