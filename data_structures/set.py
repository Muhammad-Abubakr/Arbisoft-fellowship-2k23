# unordered, unchangeable, does not allow duplicates
# highly efficient to remove duplicates
# to perform common math operations like union, intersection

# Unchangeable - but whenever needed we can remove and add
# items

"""
Sets:
a) What is the key characteristic of sets that makes them different from 
    other collection types?

b) How do you add elements to a set?

c) How can you perform set intersection and union operations in Python?
"""

"""
Well done on answering the sets questions! You got most of it right:

a) Sets in Python indeed do not allow duplicates, and they are unordered 
    collections of unique elements. When you try to add a duplicate element 
    to a set, it will efficiently ignore the duplicate, and the set's contents
    remain unchanged.

b) To add elements to a set in Python, you can use the `add()` method. This 
    method takes in an element as an argument and adds it to the set. 
    Example: `my_set.add(42)`.

c) For set union and intersection operations in Python, we use the `union()` 
    and `intersection()` methods, respectively. When calling these methods, we
    perform the operation on the first set (entity calling the method) and pass the
    second set as an argument. These methods return a new set that contains the 
    elements resulting from the union or intersection of the two sets.

    For example:

    ```python
    set1 = {1, 2, 3}
    set2 = {3, 4, 5}

    # Union of set1 and set2
    union_set = set1.union(set2)
    print(union_set)  # Output: {1, 2, 3, 4, 5}

    # Intersection of set1 and set2
    intersection_set = set1.intersection(set2)
    print(intersection_set)  # Output: {3}
    ```

Well done on providing the complete answer! If you have any more questions, 
need further explanations, or want to explore other topics, feel free to let me know.
Keep up the excellent learning!

You are correct in your understanding. When performing set operations like union
and intersection, Python creates a new set to store the result, which means 
additional memory allocation is required. The original sets remain unchanged 
unless they are no longer being referred to and are eligible for garbage collection.

Let's break down the space complexity of the union and intersection operations:

1. **Union**:
   - The `union()` method creates a new set to store the result of the union.
   - The space cost of the new set is proportional to the total number of unique
   elements in both sets, including duplicates. So, in the worst case, the new 
   set may have a size of O(n + m), where n is the number of elements in the first
   set and m is the number of elements in the second set.
   - The original sets (set1 and set2) are not modified and retain their original sizes.
   Therefore, the space cost for the two original sets is O(n) + O(m).

2. **Intersection**:
   - The `intersection()` method creates a new set to store the result of the intersection.
   - The space cost of the new set is proportional to the number of elements that are
   common in both sets. In the worst case, the new set may have a size of O(min(n, m)),
   where n is the number of elements in the first set and m is the number of elements in
   the second set.
   - The original sets (set1 and set2) are not modified and retain their original sizes. 
   Therefore, the space cost for the two original sets is O(n) + O(m).

In summary, the space complexity for set union and intersection operations can be expressed as follows:

- Union: O(n + m) for the new set + O(n) + O(m) for the two original sets.
- Intersection: O(min(n, m)) for the new set + O(n) + O(m) for the two original sets.

The overall space complexity for these set operations is dominated by the size of the 
new set and remains linear (O(n + m)) or sub-linear (O(min(n, m))) with respect to the
sizes of the original sets.

Keep in mind that Python's set operations are generally efficient and well-optimized.
Unless you are dealing with extremely large sets, the memory usage for these operations
should not be a major concern. If memory usage becomes critical, consider using other 
data structures or algorithms that might better suit your specific needs.
"""