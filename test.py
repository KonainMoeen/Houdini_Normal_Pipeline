# a = {1:[1], 2:[1,2]}
# b = {3:[1,2,3], 1:[1,2], 5:[1]}

# a = [1,2,3]

# for i in a[:-1]:
#     print(i)

a = 'a_b_c'

print(a.join(a.split('_')[1:]))