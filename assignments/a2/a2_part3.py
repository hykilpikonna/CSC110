"""CSC110 Fall 2021 Assignment 2, Part 3: Generating a Timetable

Instructions (READ THIS FIRST!)
===============================
This Python module contains the functions you should complete for Part 3 of this assignment.
Your task is to complete the functions in this module, following the definitions given in
the assignment handout.

You may find it useful to write helper functions to split up your code (we've provided
some hints on places to do so below).

You may, but are not required to, write doctests for this part.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu, Mario Badr, and Tom Fairgrieve.
"""
import datetime


###################################################################################################
# Part 3, Question 1
###################################################################################################
def num_sections(course: tuple[str, str, set]) -> int:
    """Return the number of sections for the given course.

    Preconditions:
        - The input matches the format for a course described by the assignment handout.
    """
    return len(course[2])


def num_lecture_hours(section: tuple[str, str, tuple]) -> int:
    """Return the total number of lecture hours per week.

    Preconditions:
        - The input matches the format for a section described by the assignment handout.

    Hint: you can use ".hour" to access the hour attribute of a datetime.time value.
    """
    return sum(t[2].hour - t[1].hour for t in section[2])


def sections_in_semester(schedule: dict[str, tuple[str, str, tuple]], semester: str) \
        -> set[tuple[str, str, tuple]]:
    """Return the set of all sections in schedule that are taken in semester.

    Courses that are taken in both semesters (i.e., 'Y') should always be included.

    Preconditions:
        - The input matches the format for a schedule described by the assignment handout.
        - semester in {'F', 'S'}
    """
    return {section for section in schedule.values() if section[1] == semester}


###################################################################################################
# Part 3, Question 2b
###################################################################################################
def times_conflict(m1: tuple[str, datetime.time, datetime.time],
                   m2: tuple[str, datetime.time, datetime.time]) -> bool:
    """Return whether the meeting times m1 and m2 conflict.

    Hint:
        - You can use comparison operators like < and == with datetime.time objects

    Preconditions:
        - m1 and m2 match the format for a meeting described by the assignment handout.

    >>> times_conflict(('Monday', datetime.time(9), datetime.time(11)), \
                       ('Tuesday', datetime.time(9), datetime.time(11)))
    False
    >>> times_conflict(('Monday', datetime.time(8), datetime.time(10)), \
                       ('Monday', datetime.time(10), datetime.time(12)))
    False
    >>> times_conflict(('Monday', datetime.time(10), datetime.time(12)), \
                       ('Monday', datetime.time(8), datetime.time(10)))
    False
    >>> times_conflict(('Monday', datetime.time(8), datetime.time(10)), \
                       ('Monday', datetime.time(9), datetime.time(11)))
    True
    >>> times_conflict(('Monday', datetime.time(9), datetime.time(11)), \
                       ('Monday', datetime.time(8), datetime.time(10)))
    True
    >>> times_conflict(('Monday', datetime.time(8), datetime.time(10)), \
                       ('Monday', datetime.time(8), datetime.time(9)))
    True
    >>> times_conflict(('Monday', datetime.time(0), datetime.time(23)), \
                       ('Monday', datetime.time(8), datetime.time(9)))
    True
    """
    day1, start1, end1 = m1
    day2, start2, end2 = m2

    # They cannot conflict if they aren't on the same day
    # Case 1: The start times are equal, they conflict
    #   assuming each course has at least one hour of duration
    # Case 2: 1 starts earlier than 2 and 1 ends later than the start of 2, conflict
    # Case 3: 2 starts earlier than 1 and 2 ends later than the start of 1, conflict
    return day1 == day2 and end1 > start2 and end2 > start1


def sections_conflict(s1: tuple[str, str, tuple], s2: tuple[str, str, tuple]) \
        -> bool:
    """Return whether the sections s1 and s2 conflict.

    Hint:
        - Use times_conflict

    Preconditions:
        - s1 and s2 match the format for a section described by the assignment handout.
    """
    _, term1, times1 = s1
    _, term2, times2 = s2

    # Cannot conflict if they aren't in overlapping term
    # Conflicts when at least one meeting times conflict
    return (term1 == term2 or term1 == 'Y' or term2 == 'Y') and \
        any(times_conflict(m1, m2) for m1 in times1 for m2 in times2)


def is_valid(schedule: dict[str, tuple[str, str, tuple]]) -> bool:
    """Return whether the given schedule is valid.

    Hint:
        - Refer to the handout for a definition of a valid schedule

    Preconditions:
        - schedule matches the format for a schedule described by the assignment handout.
    """
    sections = schedule.values()
    return all(not sections_conflict(s1, s2) for s1 in sections for s2 in sections if s1 != s2)


def possible_schedules(c1: tuple[str, str, set], c2: tuple[str, str, set]) \
        -> list[dict[str, tuple[str, str, tuple]]]:
    """Return a list of all possible schedules of courses c1 and c2.

    Each returned schedule should contain exactly two key-value pairs, one with the course
    code and a section of c1, and the other with the course code and a section of c2.

    Invalid schedules are returned in this list.

    If a given course has no sections, then return an empty list.
    (This will happen "automatically" if you use a comprehension with an empty collection!)

    Preconditions:
        - c1 and c2 match the format for a course described by the assignment handout.
        - c1 != c2
    """
    return [{c1[0]: section1, c2[0]: section2} for section1 in c1[2] for section2 in c2[2]]


def valid_schedules(c1: tuple[str, str, set],
                    c2: tuple[str, str, set]) \
        -> list[dict[str, tuple[str, str, tuple]]]:
    """Return a list of all VALID schedules of courses c1 and c2.

    Each returned schedule should contain exactly two key-value pairs, one with the course
    code and a section of c1, and the other with the course code and a section of c2.

    Invalid schedules are NOT returned in this list.

    Hint:
        - Use is_valid
        - Use possible_schedules

    Preconditions:
        - c1 and c2 match the format for a course described by the assignment handout.
        - c1 != c2
    """
    schedules = possible_schedules(c1, c2)
    return [x for x in schedules if is_valid(x)]


def possible_five_course_schedules(c1: tuple[str, str, set],
                                   c2: tuple[str, str, set],
                                   c3: tuple[str, str, set],
                                   c4: tuple[str, str, set],
                                   c5: tuple[str, str, set]) -> list[dict[str, tuple]]:
    """Return a list of every possible schedule that contains all given courses.

    This is analogous to possible_schedules, except now there are 5 courses instead of 2.

    If a given course has no sections, then return an empty list.
    (This will happen "automatically" if you use a comprehension with an empty collection!)

    Preconditions:
        - all given courses match the format for a course described by the assignment handout.
        - c1 != c2 and c1 != c3 and c1 != c4 and c1 != c5
        - c2 != c3 and c2 != c4 and c2 != c5
        - c3 != c4 and c3 != c5
        - c4 != c5

    HINT: you'll want a comprehension with 5 different variables. You can split up each
    "for ... in ..." across multiple lines to help make your code more readable.
    """
    return [{c1[0]: a, c2[0]: b, c3[0]: c, c4[0]: d, c5[0]: e}
            for a in c1[2] for b in c2[2] for c in c3[2] for d in
            c4[2] for e in c5[2]]


def valid_five_course_schedules(c1: tuple[str, str, set],
                                c2: tuple[str, str, set],
                                c3: tuple[str, str, set],
                                c4: tuple[str, str, set],
                                c5: tuple[str, str, set]) -> list[dict[str, tuple]]:
    """Return a list of every valid schedule that contains all given courses.

    This is analogous to valid_schedules, except now there are 5 courses instead of 2.

    Hint:
        - Use is_valid
        - Use possible_five_course_schedules

    Preconditions:
        - all given courses match the format for a course described by the assignment handout.
        - c1 != c2 and c1 != c3 and c1 != c4 and c1 != c5
        - c2 != c3 and c2 != c4 and c2 != c5
        - c3 != c4 and c3 != c5
        - c4 != c5
    """
    schedules = possible_five_course_schedules(c1, c2, c3, c4, c5)
    return [x for x in schedules if is_valid(x)]


###################################################################################################
# Part 3, Question 3b
###################################################################################################
def is_section_compatible(schedule: dict[str, tuple[str, str, tuple]],
                          section: tuple[str, str, tuple]) -> bool:
    """Return whether the given section is compatible with the given schedule.

    Hint:
        - Refer to the handout for a definition of compatibility
        - Use sections_conflict
        - You can get a collection of only the values of a dict by using dict.values

    Preconditions:
        - section matches the format for a section described by the assignment handout.
        - schedule matches the format for a schedule described by the assignment handout.
    """
    return all(not sections_conflict(section, s) for s in schedule.values())


def is_course_compatible(schedule: dict[str, tuple[str, str, tuple]],
                         course: tuple[str, str, set]) -> bool:
    """Return whether the given course is compatible with the given schedule.

    Hint:
        - Refer to the handout for a definition of compatibility
        - Use is_section_compatible

    Preconditions:
        - course matches the format for a course described by the assignment handout.
        - schedule matches the format for a schedule described by the assignment handout.
        - course[0] not in schedule
    """
    return any(is_section_compatible(schedule, section) for section in course[2])


def compatible_sections(schedule: dict[str, tuple[str, str, tuple]],
                        course: tuple[str, str, set]) -> set[tuple[str, str, tuple]]:
    """Return the set of sections of the given course that are compatible with the given schedule.

    Hint:
        - Refer to the handout for a definition of compatibility
        - Use is_section_compatible

    Preconditions:
        - course matches the format for a course described by the assignment handout.
        - schedule matches the format for a schedule described by the assignment handout.
        - course[0] not in schedule
    """
    return {section for section in course[2] if is_section_compatible(schedule, section)}


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # IMPORTANT: Leave this code uncommented when you submit your files.
    python_ta.check_all(config={
        'extra-imports': ['datetime', 'python_ta.contracts'],
        'max-line-length': 100,
        'disable': ['R1705', 'R1729']
    })
