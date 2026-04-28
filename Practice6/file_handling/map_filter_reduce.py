from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map
doubled = list(map(lambda x: x * 2, numbers))

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))

# reduce
total = reduce(lambda x, y: x + y, numbers)

print(doubled)
print(even)
print(total)