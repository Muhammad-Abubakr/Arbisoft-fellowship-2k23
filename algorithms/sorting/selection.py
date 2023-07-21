def selection_sort(things):
    """Implementation of Selection Sort algorithm
    
    [input] = things: List<int>
    [Output] = List<int> (sorted)
    """
    sorted = -1
    currentMinimum = -1

    while sorted != len(things)-1:
        # finding the current minimum value from
        # unsorted array
        for x in range(sorted + 1, len(things)):
            if things[x] <= things[currentMinimum]:
                currentMinimum = x
        
        # swapping it with the first unsorted value
        sorted += 1
        temp = things[currentMinimum]
        things[currentMinimum] = things[sorted]
        things[sorted] = temp
        
    
    return things


print(selection_sort([3, 4, 2, 0, 98, 2, 1, 5]))