"""CSC110 Fall 2021 Assignment 4, Part 2: Generating coprime numbers

Instructions (READ THIS FIRST!)
===============================
Implement each of the functions in this file. As usual, do not change any function headers
or preconditions. You do NOT need to add doctests.

You may create additional helper functions to help break up your code into smaller parts.

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


def coprime_to_2_and_3(n: int) -> list[int]:
    """Return the natural numbers less than n that are coprime to both 2 and 3.

    The returned list is sorted.

    Preconditions:
      - n >= 6

    >>> coprime_to_2_and_3(20)
    [1, 5, 7, 11, 13, 17, 19]

    Implementation note: recall negative list indexing from Assignment 3.
    For all lists lst and integers i between 0 and len(lst) - 1 inclusive,
    lst[-i] == lst[len(lst) - i].
    """
    nums_so_far = [1, 5]
    while nums_so_far[-2] + 6 < n:
        # Note: Write four assert statements here expressing the four loop invariants from the
        # assignment handout. These statements should be at the top of the loop body.

        # Loop Invariant 1: every number k in nums_so_far is coprime to 2 and coprime to 3.
        assert all(math.gcd(k, 2) == 1 and math.gcd(k, 3) == 1 for k in nums_so_far)
        # Loop Invariant 2: for all natural numbers i between 0 and len(nums_so_far) - 3 inclusive,
        #   nums_so_far[i] + 6 == nums_so_far[i + 2].
        assert all(nums_so_far[i] + 6 == nums_so_far[i + 2] for i in range(len(nums_so_far) - 2))
        # Loop Invariant 3: for all natural numbers i between 0 and len(nums_so_far) - 2 inclusive,
        #   nums_so_far[i] < nums_so_far[i + 1] (this means that nums_so_far is always sorted).
        assert all(nums_so_far[i] < nums_so_far[i + 1] for i in range(len(nums_so_far) - 1))
        # Loop Invariant 4: for all natural numbers k between 0 and nums_so_far[-1] inclusive,
        #   if k is coprime to 2 and coprime to 3, then k in nums_so_far.
        assert all(k in nums_so_far for k in range(nums_so_far[-1] + 1)
                   if math.gcd(k, 2) == 1 and math.gcd(k, 3) == 1)

        next_number = nums_so_far[-2] + 6
        list.append(nums_so_far, next_number)

    return nums_so_far


def coprime_to_all(primes: set[int], n: int) -> list[int]:
    """Return the positive integers less than n that are coprime to every number in primes.

    The returned list is sorted.

    Pay attention to the preconditions, as they are designed to help simplify your work for this
    question.

    Preconditions:
        - primes != set()
        - every element of primes is prime
        - n >= math.prod(primes)

    >>> coprime_to_all({2, 3}, 20)
    [1, 5, 7, 11, 13, 17, 19]
    >>> coprime_to_all({2, 3, 7}, 50)
    [1, 5, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41, 43, 47]

    Implementation notes:
        - You MUST use the provided helper function starting_coprime_numbers in your implementation,
          and may NOT modify it (even though it is not as efficient as it could be!!).
        - You will find the math.prod function useful.
    """
    m = math.prod(primes)
    nums_so_far = starting_coprime_numbers(primes)
    k = len(nums_so_far)
    while nums_so_far[-k] + m < n:
        # Note: Write four assert statements here expressing the four loop invariants from the
        # assignment handout. These statements should be at the top of the loop body.

        # Loop Invariant 1: every number k in nums_so_far is coprime to every prime
        assert all(all(math.gcd(p, k) == 1 for p in primes) for k in nums_so_far)
        # Loop Invariant 2: for all natural numbers i between 0 and
        #   len(nums_so_far) - k - 1 inclusive,
        #   nums_so_far[i] + m == nums_so_far[i + k].
        assert all(nums_so_far[i] + m == nums_so_far[i + k]
                   for i in range(len(nums_so_far) - k))
        # Loop Invariant 3: for all natural numbers i between 0 and len(nums_so_far) - 2 inclusive,
        #   nums_so_far[i] < nums_so_far[i + 1] (this means that nums_so_far is always sorted).
        assert all(nums_so_far[i] < nums_so_far[i + 1] for i in range(len(nums_so_far) - 2 + 1))
        # Loop Invariant 4: for all natural numbers k between 0 and nums_so_far[-1] inclusive,
        #   if k is coprime to all primes, then k in nums_so_far.
        assert all(k in nums_so_far for k in range(nums_so_far[-1] + 1)
                   if all(math.gcd(p, k) == 1 for p in primes))

        next_number = nums_so_far[-k] + m
        list.append(nums_so_far, next_number)

    return nums_so_far


def starting_coprime_numbers(primes: set[int]) -> list[int]:
    """Return the numbers up to the product of the given primes that are coprime to all of them.

    Note: the length of the returned list is is exactly equal to phi(math.prod(primes)), where
    phi is the Euler totient function.

    Preconditions:
        - primes != set()
        - every element of primes is prime

    >>> starting_coprime_numbers({2, 3})
    [1, 5]
    >>> starting_coprime_numbers({3, 11})
    [1, 2, 4, 5, 7, 8, 10, 13, 14, 16, 17, 19, 20, 23, 25, 26, 28, 29, 31, 32]
    """
    nums_so_far = []
    m = math.prod(primes)

    for k in range(1, m):
        is_coprime = True
        for p in primes:
            if k % p == 0:
                is_coprime = False
        if is_coprime:
            list.append(nums_so_far, k)

    return nums_so_far


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'math'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import doctest
    doctest.testmod()
