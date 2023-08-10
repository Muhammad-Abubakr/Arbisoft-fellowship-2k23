# ordered, changeable, allow duplicates
# dynamically sized

"""
Great! Let's go through the answers for the section about Lists:

1. **Lists**:

a) How do you add an element to the end of a list in Python?
    **Answer**: You can use the `append()` method to add an element
    to the end of a list. For example:
    ```python
    my_list = [1, 2, 3]
    my_list.append(4)
    print(my_list)  # Output: [1, 2, 3, 4]
    ```

b) What is the time complexity of appending an element to the end of a list?
    **Answer**: The `append()` method has an amortized time complexity of O(1). 
    This means that on average, it takes constant time to add an element to the 
    end of the list. However, in some cases, the `append()` operation may trigger
    a resizing of the list (to accommodate more elements), which takes O(n) time.
    The resizing operation is done infrequently to ensure that the average time 
    complexity remains constant.

c) How do you remove an element from a list by its value?
    **Answer**: You can use the `remove()` method to remove the first occurrence
    of a specific value from the list. For example:
    ```python
    my_list = [1, 2, 3, 2, 4]
    my_list.remove(2)
    print(my_list)  # Output: [1, 3, 2, 4]
    ```
Note that the `remove()` method raises a `ValueError` if the specified value is not found
in the list. If you want to remove an element by its index, you can use the `del` statement
or the `pop()` method.

Great job on answering the questions about lists! If you're ready, feel free to tackle the
questions on tuples, dictionaries, sets, and strings. If you have any doubts or need further
explanations, don't hesitate to ask! Happy learning!
"""