from compiler.execution import *
from example_simulations.example_1 import *#decisions ,categories,distributions,nations,events


t = cp_time.time()
a = Code()
a.compile(categories + distributions + nations + events + decisions + 'simulate(100d,5);')

print("total time",cp_time.time()-t)