def reversed_string(str):
    """Function that reverses the given String
    
    [Input] = str: String
    [Output] = str: String; reversed
    """
    return str[::-1]
    

def is_palindrome(str):
    """Function that checks whether a given string is a Palindrome or
    not.
    
    [Input] = str: String
    [Output] = bool; indicating whether input is Palindrome or not
    """
    if(len(str)//2 == 0):
        if str[: len(str)//2-1 : -1] == str[: len(str)//2]:
            return True
    else:
        if str[: len(str)//2 : -1] == str[: len(str)//2]:
            return True
        
    return False 


def sort_alphabetically(str):
    """Function that sorts the given String alphabetically, has two sub
    functions. `sorter` and `merge`
    
    [Input] = str: String
    [Output] = String (sorted alphabetically)
    """
    words = str.split(' ')
        
    return " ".join(sorter(words)) 


def sorter(words):
    """Sorter uses the Divide and Conquer analogy for sorting the given
    list of words. Specifically it utilizes the MergeSort algorithm.
    
    [Input] = words: List<String>
    [Output] = List<String> (sorted alphabetically)
    """
        
    if len(words) <= 1:
        return words

    else:
        first_half = sorter(words[: len(words)//2]) 
        second_half = sorter(words[len(words)//2 :])
        
        # merge the two arrays
        return merge(first_half, second_half)
        
def merge(a,b):
    """Function that merges the two sorted arrays into one array that
    is also sorted.
    
    [Input] = a: List<String>, b: List<String>
    [Output] = c: List<String>
    """
    c = []
    
    # While either of two arrays, one becomes empty. Compare corresponding
    # elements and append the smaller to the array `c` while removing it from
    # the original array
    while len(a) != 0 and len(b) != 0:
        if ord(a[0]) < ord(b[0]):
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    
    # If `b` was empty and `a` still had elements, include them
    while len(a) != 0:  
        c.append(a[0])
        a.remove(a[0])
        
    # If `a` was empty and `b` still had elements, include them
    while len(b) != 0:
        c.append(b[0])
        b.remove(b[0])
        
    return c

     
print(reversed_string('Hello World!'))

print(is_palindrome('abba'))

print(sort_alphabetically("f e h a u b"))