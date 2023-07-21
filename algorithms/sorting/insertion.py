def insertion_sort(things):
    """ This sorting algorithm works by dividing the array into two 
    parts theoretically. 
    i). Sorted (left) 
    ii). Unsorted (right)
    
    Everytime we perform an iteration we take an element from the un-
    sorted list and find an appropriate place for it (in this algorithm
    using Binary Search), shift the elements and place it in sorted part.
    """
    for i in range(1, len(things)):
        test_element = things[i]
        
        # using the binary search algorithm to find a suitable place 
        # for our selected element in the sorted part of our array
        l = 0
        r = i
        
        while l<=r:
            m = (l+r)//2
            if test_element > things[m]:
                l = m + 1
            else:
                r = m - 1
        
        # shifting elements to right, to make space for test_element
        for j in range(i, l-1, -1):
            things[j] = things[j-1]

        # assinging the test_element to the space made after shifting
        things[l] = test_element
        
    return things

print(insertion_sort([3, 4, 2, 0, 98, 2, 1, 5]))