from map import *


m = Map()
m.add_province('Matanzas', 10, 10, 120)
m.add_province('Habana', 14, 15, 240, ['Matanzas'])
m.add_province('Camaguey', 12, 12, 100, ['Matanzas', 'Habana'])
m.add_nation('Cuba', ['Matanzas', 'Habana', 'Camaguey'])
m.add_province('Florida', 10, 10, 120)


m.update('Habana', development= 20)
m.update('Cuba', provinces= ['Florida'])

nat: Nation= m.nationdict['Cuba']
print(m.mapelementsdict)


