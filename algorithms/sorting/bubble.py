def bubble_sort(things):
    """Implementation of Bubble Sort algorithm
    
    [input] = things: List<int>
    [Output] = List<int> (sorted)
    """
    for i in range(len(things)):
        for j in range(len(things)-1):
            if things[j] > things[j+1]:
                things[j+1] += things[j]
                things[j] = things[j+1] - things[j]
                things[j+1] -= things[j]

    return things


print(bubble_sort([2, 8, 5, 3, 9, 4, 1]))