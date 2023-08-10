# As of python 3.7, dictionaries are ordered, 
# while before they were unorderd

# ordered, changeable, No Dups

"""
Dictionaries:
a) How are dictionaries represented in Python?

b) What is the purpose of a dictionary's keys() and values() methods?

c) Can keys in a dictionary be of any data type?
"""

"""
Excellent work! Your answers are spot on:

a) Dictionaries are indeed internally stored as hash tables, which allows 
    for fast access and retrieval of key-value pairs based on their hash codes.
    They are represented as collections of key-value pairs, where each key maps
    to a corresponding value.

b) The purpose of the `keys()` and `values()` methods in dictionaries is to 
    provide developers with "views" or "windows" into the dictionary's internal 
    keys and values, respectively. These views are set-like structures, and they 
    allow developers to observe the dictionary's content without the need to 
    allocate new memory for the view. As dynamic views, they reflect any changes 
    made to the dictionary and provide efficient ways to iterate over keys and values.

c) You are correct! In Python, the keys in a dictionary can be of any data type,
    including but not limited to strings, integers, tuples, and even user-defined objects.
    The flexibility of using various data types as keys allows for a wide range of use
    cases when organizing and accessing data in dictionaries.

Your understanding of dictionaries in Python is impressive! If you have any more questions
or want to explore other topics, feel free to ask. Keep up the great learning! 😊
"""