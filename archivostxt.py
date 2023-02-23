# f=open('Alumnos.txt', 'r')
# alumnos=f.read()
# print(alumnos)
# f.seek(0)
# alumnos2=f.read()
# print(alumnos2)
# alumnos=f.readline()
# print(alumnos)
# for item in alumnos:
#     print(item,end='')

f=open('Alumnos2.txt', 'w')
f.write('\n'+'Hola mundo')
f.write('\n'+'Nuevo hola mundo')

f.close()