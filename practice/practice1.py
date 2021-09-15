"""CSC110 Extra MarkUs Practice Questions - Week 1

Instructions (READ THIS FIRST!)
===============================

Complete the functions in this module according to their docstring.

We have marked each place you need to write code with the word
As you complete your work in this file, delete each TO-DO comment---this is a
good habit to get into early! To check your work, you should run this file in
the Python console and then call each function manually.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.
"""


def negate(numbers: set[float]) -> dict[float, float]:
    """Return a dictionary mapping each number in numbers to its negation.

    >>> negate({-3.50, 1.10, 11.1})
    {-3.50: 3.50, 1.10: -1.10, 11.1: -11.1}
    """
    return {number: -number for number in numbers}


if __name__ == '__main__':
    # Test code
    assert negate({-3.50, 1.10, 11.1}) == {-3.50: 3.50, 1.10: -1.10, 11.1: -11.1}
