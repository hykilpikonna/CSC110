"""CSC110 Fall 2021 Assignment 1, Part 2: Programming Exercises

Instructions (READ THIS FIRST!)
===============================

Note: these instructions are essentially the same as Prep 2, so we strongly recommend
completing the Prep 2 Programming Exercises first before starting this part.

This Python module contains the functions you should complete for Part 2 of this assignment.
Your task is to complete this module by doing the following for EACH function below:

1. Add a new doctest example to the function description in the space provided.
   This will ensure you understand what the function is supposed to do.
   (You may add more than one doctest for testing purposes if you wish.)
2. Write the body of the function so that it does what its description claims.

In some function descriptions, we have written "You may ASSUME..." This means that
when you are writing each function body, you only have to consider possible values
for the parameters that satisfy these assumptions.

By the way, we *will* be checking that you've added new doctest examples, and that
your examples correctly illustrate a call to that function. Don't skip this!

For instructions on checking your work with both doctest and python_ta, please check
the assignment handout.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu, Mario Badr, and Tom Fairgrieve.
"""
import math


def find_roots_quadratic(a: float, b: float, c: float) -> set:
    """Return a set containing the solutions to the equation ax^2 + bx + c = 0.

    Each solution is a float.

    You may ASSUME that:
      - a != 0
      - (b * b) - (4 * a * c) >= 0

    >>> find_roots_quadratic(1, -15, 56) == {8.0, 7.0}
    True
    >>> find_roots_quadratic(1, -10, 21) == {3.0, 7.0}
    True
    >>> find_roots_quadratic(1, 8, 15) == {-3.0, -5.0}
    True
    >>> # Have to use isclose to compare floats
    >>> all([math.isclose(sol, -0.739, abs_tol=0.001) or math.isclose(sol, 1.739, abs_tol=0.001) for sol in find_roots_quadratic(7, -7, -9)])
    True

    Hint: use the quadratic formula.
    """
    assert a != 0
    assert (b * b) - (4 * a * c) >= 0
    part = math.sqrt(b * b - 4 * a * c)
    return {(-b - part) / (2 * a), (-b + part) / (2 * a)}


def intersect_all(set1: set, set2: set, set3: set) -> set:
    """Return the intersection of all three of the given sets: set1, set2, and set3.

    >>> intersect_all({1, 2, 3}, {1, 2, 3, "test"}, {1, 2, 6, 7, "test"}) == {1, 2}
    True
    >>> intersect_all(set(), {1, 2, 3}, {1, 2, 3}) == set()
    True
    >>> intersect_all({"a", ""}, {1, 0}, {True, False}) == set()
    True
    >>> intersect_all({'a'}, {"a"}, {chr(97)}) == {'a'}
    True
    """
    return set.intersection(set1, set2, set3)


def greet_all(greeting: str, names: list) -> list:
    """Return a list of strings that consist of the greeting messages for each person in names.

    The format of each greeting message is '<greeting>, <name>',
    where greeting is the given greeting and <name> is an element of <names>.

    The returned list should contain the greetings for the names in the same order each name
    appears in the given names list.

    You may ASSUME that:
        - names is either empty or contains elements that are strings

    >>> greet_all('Good morning', ['Alan Turing', 'Grace Hopper'])
    ['Good morning, Alan Turing', 'Good morning, Grace Hopper']
    >>> greet_all('', [])
    []
    >>> greet_all('<greeting>', ['<name>'])
    ['<greeting>, <name>']
    >>> greet_all('', ['', ''])
    [', ', ', ']
    """
    # assert all([isinstance(name, str) for name in names])
    return [f'{greeting}, {name}' for name in names]


def all_smaller(nums1: set, nums2: set) -> bool:
    """Return whether every number in nums1 is less than every number in num2.

    You may ASSUME that:
      - nums1 is non-empty
      - nums2 is non-empty
      - nums1 and nums2 contain only integers and/or floats

    >>> all_smaller({2}, {3})
    True
    >>> all_smaller({3}, {2})
    False
    >>> all_smaller({2, 3}, {2, 3})
    False
    >>> all_smaller({1, 2, 3}, {4, 5, 6})
    True
    >>> all_smaller({-100, -101}, {-1, 0})
    True
    >>> all_smaller({0.11}, {0.1})
    False
    >>> all_smaller({-0.01}, {-0.009})
    True

    Hint: use the min and max functions.
    """
    assert len(nums1) != 0
    assert len(nums2) != 0
    return max(nums1) < min(nums2)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100
    })
