def fibonacci(num):
    """Generates the fibonacci sequence up to the given number
    
    [input] = num: integer
    [output] = List<int> (fibonacci)
    """
    # Input validation
    if not isinstance(num, int):
        print("Please enter an Integer")
        return
    
    series = [0]
    next_num = 1
    
    while next_num < num:
        series.append(next_num)
        next_num = next_num + series[-2]
    
    return series

print(fibonacci(9))