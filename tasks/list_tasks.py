def max_value(things):
    current_max = 0
    
    for x in range(len(things)):
        if things[x] > things[current_max]:
            current_max = x
            
    return things[current_max]

print(max_value([2, 8, 5, 3, 9, 4, 1]))

