"""CSC110 Fall 2021: Term Test 2, Question 1 (Cryptography)

Module Description
==================
This module contains instructions for this question. There are THREE
parts of this question, labelled "Part (a)", "Part (b)", etc.
The comments in this file contain instructions on how to complete each part,
so please read those comments carefully.

At the bottom of the file we've provided code to run doctest and python_ta.
python_ta is not required for grading.

SUBMIT THIS FILE FOR GRADING!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Mario Badr and Tom Fairgrieve.
"""


###################################################################################################
# Encrypting Grade Messages
###################################################################################################
# We can represent your first-year courses grades using a tuple of five integers between 0 and 100,
# inclusive. A *grades message* is a list of grades, i.e., a list[tuple[int, int, int, int, int]].
# For example:
#
#    [(95, 90, 67, 75, 89), (55, 64, 78, 92, 86), (100, 96, 64, 83, 87)]

###################################################################################################
# Description of the Cryptosystem
###################################################################################################
# We define the following SYMMETRIC-KEY CRYPTOSYSTEM on grade messages:
#
# PLAINTEXT and CIPHERTEXT:
#   Grades messages (i.e, list[tuple[int, int, int, int, int]],
#   where each int is in 0-100, inclusive.
#
# SECRET KEY:
#   The secret key is an integer k.
#
# ENCRYPTION:
#   For each index i in the plaintext grade message (starting at i = 0), transform the i-th grade
#   tuple by adding (k^(i+1)) to each element of the tuple and then taking the remainder modulo 101.
#
# DECRYPTION:
#   Reverse the encryption process.

###################################################################################################
# Part (a) - encryption
###################################################################################################
# The function below is the start of the encryption algorithm described above.
# Complete it by doing two things:
#   1. Complete the doctest example by showing the expected return value of the function call.
#   2. Implement the function body. You may use loops, comprehensions, and/or helper functions.
#      You are not required to add doctests for any helper functions you create.
#
#      Note: encryption should NOT mutate the input plaintext.


def encrypt_tt2(k: int, plaintext: list[tuple[int, int, int, int, int]]) \
        -> list[tuple[int, int, int, int, int]]:
    """Return the ciphertext grade message when plaintext is encrypted with key k.

    Preconditions:
        - k and plaintext are valid inputs for encryption, based on the cryptosystem description

    >>> key = 20
    >>> p = [(95, 90, 67, 75, 89), (55, 64, 78, 92, 86)]
    >>> encrypt_tt2(key, p)
    [(14, 9, 87, 95, 8), (51, 60, 74, 88, 82)]
    """
    c = []
    for i in range(len(plaintext)):
        incr = k ** (i + 1)
        n1, n2, n3, n4, n5 = [(n + incr) % 101 for n in plaintext[i]]
        c.append((n1, n2, n3, n4, n5))
    return c


###################################################################################################
# Part (b) - decryption
###################################################################################################
# The function below is the start of the decryption algorithm described above.
# Complete it by doing two things:
#   1. Add one new doctest example for this function.
#   2. Implement the function body. You may use loops, comprehensions, and/or helper functions.
#      You are not required to add doctests for any helper functions you create.
#      It is up to you to determine the correct algorithm for decrypting a ciphertext,
#      based on the description of the encryption algorithm.
#
#      Note: decryption should NOT mutate the input ciphertext.

def decrypt_tt2(k: int, ciphertext: list[tuple[int, int, int, int, int]]) \
        -> list[tuple[int, int, int, int, int]]:
    """Return the plaintext grade message when ciphertext is decrypted with key k.

    Preconditions:
        - k and ciphertext are valid inputs for decryption, based on the cryptosystem description

    >>> key = 20
    >>> c = [(19, 15, 84, 2, 6)]
    >>> decrypt_tt2(key, c)
    [(100, 96, 64, 83, 87)]
    """
    p = []
    for i in range(len(ciphertext)):
        incr = k ** (i + 1)
        n1, n2, n3, n4, n5 = [(n - incr) % 101 for n in ciphertext[i]]
        p.append((n1, n2, n3, n4, n5))
    return p


###################################################################################################
# Part (c) - understanding the cryptosystem
###################################################################################################
def why_101() -> str:
    """Return a string describing why we use a modulus of 101 instead of 100 in the cryptosystem
    defined above.
    """
    return "This is because modding by 100 will return the last two digits of the original number" \
           ", which will reveal the original content if the key is a whole number like 10 or 20"
