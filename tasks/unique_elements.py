def unique_elements(elements):
    """ Takes in a list of elements and return unique elements list while
    preserving the order.
    
    [Input] = elements: List<T>
    [Output] = List<T> (unique)
    """
    unique = []
    for x in elements:
        if x not in unique:
            unique.append(x)
    
    return unique
    
print(unique_elements([2,3,2,3,1,2]))