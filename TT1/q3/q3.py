"""CSC110 Fall 2021: Term Test 1, Q3

Module Description
==================
This Python file contains instructions for this question. There are FOUR
parts of this question, labelled "Part (a)", "Part (b)", etc.
The docstrings in this file contain instructions on how to complete each part,
so please read those comments carefully.

python_ta is not required for grading.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Mario Badr and Tom Fairgrieve.
"""
from dataclasses import dataclass


####################################################################################################
# Part (a)
####################################################################################################
def create_nested_list_data() -> list[list]:
    """Return a small dataset in a nested list format.

    Each nested list is composed of items with type: str, str, float, in that order.
        - The first str is the title (i.e., name) of a book
        - The second str is the name of the author
        - the float is the average rating for the book

    INSTRUCTIONS: Do NOT change this function.
    """
    return [
        ['Shogun', 'James Clavell', 4.39],
        ['1984', 'George Orwell', 4.4],
        ['Animal Farm', 'George Orwell', 3.96],
        ['The Ex Hex', 'Erin Sterling', 3.76]
    ]


def comma_separated_titles(data: list[list]) -> str:
    """Return a string of the book titles in data in the order that they appear, where each title
    ends with a comma and a space (i.e., ', ').

    Preconditions:
        - data is in the format as specified in create_nested_list_data

    INSTRUCTIONS: Complete the body of this function. You must follow the docstring description
        exactly. Do NOT add any more doctest examples.

    RESTRICTIONS:
        - You must use a for loop
        - You may not use any comprehensions
        - You may not use any built-in functions/methods

    >>> example_data = create_nested_list_data()
    >>> comma_separated_titles(example_data)
    'Shogun, 1984, Animal Farm, The Ex Hex, '
    """
    csv = ""
    for entry in data:
        csv += entry[0] + ', '
    return csv


def reset_ratings(data: list[list], author: str) -> None:
    """Reset (i.e., MUTATE) the ratings of all books by author in data to 0.0.

    Preconditions:
        - data is in the format as specified in create_nested_list_data

    INSTRUCTIONS: Complete the body of this function and add ONE doctest example that demonstrates
        what the function does.

    RESTRICTIONS:
        - You must use a for loop
        - You may not use any comprehensions
        - You may not use any built-in functions/methods

    >>> example_data = create_nested_list_data()
    >>> reset_ratings(example_data, 'George Orwell')
    >>> example_data[1][2] == 0.0 and example_data[2][2] == 0.0
    True
    """
    for entry in data:
        if entry[1] == author:
            entry[2] = 0.0


####################################################################################################
# Part (b)
####################################################################################################
def has_valid_ratings(data: list[list]) -> bool:
    """Return whether every rating in data is a valid rating.

    A valid rating is a rating between 0.0 and 5.0, inclusive.

    Preconditions:
        - data is in the format as specified in create_nested_list_data
        - len(data) > 0

    INSTRUCTIONS: Do NOT change this function. We know that it contains at least one bug.
    """
    for book in data:
        if 0.0 <= book[2] <= 5.0:
            return False

    return True


def test_has_valid_ratings() -> None:
    """Test has_valid_ratings (see instructions).

    INSTRUCTIONS: There is at least one bug in has_valid_ratings. Complete the body of this UNIT
        TEST so that it demonstrates a bug. That is, this unit test should fail when run on
        has_valid_ratings.

    RESTRICTIONS:
        - You may not use hypothesis
        - You may not violate the function's preconditions (including the type contract)
    """
    data = create_nested_list_data()
    assert has_valid_ratings(data)


def has_valid_ratings_bug() -> str:
    """Return a BRIEF English description of the bug you found in has_valid_ratings.

    INSTRUCTIONS: Complete the body of this function so that it returns your description of the
        bug in a single string.

    RESTRICTIONS:
        - Your description must be less than 200 characters (i.e.,
            len(has_valid_ratings_bug()) < 200)
    """
    return "The body should not return False when it found a valid rating (between 0 and 5), it should return false when it found an invalid rating instead."


####################################################################################################
# Part (c)
####################################################################################################
@dataclass
class Book:
    """A data class that represents a book at Indigo.

    INSTRUCTIONS: Do NOT change this dataclass.

    Instance Attributes:
        - title: the title (or name) of the book
        - author: the name of the author of the book
        - rating: the average rating of the book

    Representation Invariants:
        - self.title != ''
        - self.author != ''
        - self.rating >= 0.0

    >>> some_book = Book('1984', 'George Orwell', 4.4)
    """
    title: str
    author: str
    rating: float


def create_dataclass_data() -> list[Book]:
    """Return a small dataset in a list of dataclass format.

    INSTRUCTIONS: Do NOT change this function.
    """
    return [
        Book('Shogun', 'James Clavell', 4.39),
        Book('1984', 'George Orwell', 4.4),
        Book('Animal Farm', 'George Orwell', 3.96),
        Book('The Ex Hex', 'Erin Sterling', 3.76)
    ]


def collect_ll_authors(data: list[Book]) -> set[str]:
    """Return the set of all author names in data where the author name contains two adjacent
    lowercase l's (i.e., 'll').

    INSTRUCTIONS: Complete the body of this function and add ONE doctest example that demonstrates
        what the function does.

    RESTRICTIONS:
        - You must use a for loop
        - You may not use any comprehensions
        - You may not use any built-in functions/methods, EXCEPT FOR: set.add

    >>> example_data = create_dataclass_data()
    >>> collect_ll_authors(example_data) == {'James Clavell', 'George Orwell'}
    True
    """
    ll_authors = set()
    for entry in data:
        if 'll' in entry.author:
            ll_authors.add(entry.author)
    return ll_authors


####################################################################################################
# Part (d)
####################################################################################################
def add_book_titles(titles: list[str], data: list[Book], author: str) -> None:
    """Add (i.e., MUTATE) to titles, in the order that they appear, the names of the books from data
     that are written by author.

    INSTRUCTIONS: Do NOT change this function. We know that it contains at least one bug.
    """
    for book in data:
        if book.author == author:
            titles = titles + [book.title]


def test_add_book_titles() -> None:
    """Test add_book_titles.

    INSTRUCTIONS: There is at least one bug in add_book_titles. Complete the body of this UNIT
        TEST so that it demonstrates a bug. That is, this unit test should fail when run on
        add_book_titles.

    RESTRICTIONS:
        - You may not use hypothesis
        - You may not violate the function's preconditions (including the type contract)
    """
    titles: list[str] = []
    data = create_dataclass_data()
    add_book_titles(titles, data, 'George Orwell')
    assert titles == ['1984', 'Animal Farm']


def add_book_titles_bug() -> str:
    """Return a BRIEF English description of the bug you found in add_book_titles.

    INSTRUCTIONS: Complete the body of this function so that it returns your description of the
        bug in a single string.

    RESTRICTIONS:
        - Your description must be less than 200 characters (i.e., len(add_book_titles_bug()) < 200)
    """
    return "The docstring said that it should mutate the titles list, but it did not mutate the list. It created a new list each time a matching author is found. It should use list.append instead."
