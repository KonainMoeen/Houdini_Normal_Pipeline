a = {1:[1], 2:[1,2]}
b = {3:[1,2,3], 1:[1,2]}

#a.update(b)
b = {}
a.update(b)
print(a)