from compiler.execution import *
from example_simulation.decisions import decisions 
from example_simulation.categories import categories 
from example_simulation.distributions import distributions 
from example_simulation.nations import nations 
from example_simulation.events import events 

t=cp_time.time()
a= Code()
a.compile(categories+distributions+nations+events+decisions + 'simulate(50d,5);')

print("total time",cp_time.time()-t)