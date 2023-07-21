def merge_sort(things):
    """Implements the MergeSort algorithm.
    
    [Input] = words: List<String>
    [Output] = List<String> (sorted alphabetically)
    """
    if len(things) <= 1:
        return things

    alpha = merge_sort(things[: len(things)//2])
    beta = merge_sort(things[(len(things)//2) :])

    return merge(alpha, beta)


def merge(a,b):
    """Function that merges the two sorted arrays into one array that
    is also sorted.
    
    [Input] = a: List<String>, b: List<String>
    [Output] = c: List<String>
    """
    c = []
    
    while len(a) != 0 and len(b) != 0:
        if a[0] < b[0]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    
    while len(a) != 0:
        c.append(a[0])
        a.remove(a[0])
        
    while len(b) != 0:
        c.append(b[0])
        b.remove(b[0])
        
    return c


print(merge_sort([3, 4, 2, 0, 98, 2, 1, 5]))