"""CSC110 Fall 2021 Assignment 2, Part 3: Programming Tests

Instructions (READ THIS FIRST!)
===============================
This Python module contains example tests you can run for Part 3 of this assignment. Please note
that passing all these tests does NOT mean you have a 100% correct solution.

Some of the tests are empty, consider completing them. Also consider adding more of your own tests.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu, Mario Badr, and Tom Fairgrieve.
"""
import pytest
import datetime

import a2_part3 as a2_courses
import a2_part4

###################################################################################################
# Sample Meeting Times
###################################################################################################
MON_9_TO_11 = ('Monday', datetime.time(9), datetime.time(11))
MON_12_TO_1 = ('Monday', datetime.time(12), datetime.time(13))

TUE_9_TO_11 = ('Tuesday', datetime.time(9), datetime.time(11))
TUE_10_TO_12 = ('Tuesday', datetime.time(10), datetime.time(12))

WED_9_TO_11 = ('Wednesday', datetime.time(9), datetime.time(11))
WED_12_TO_1 = ('Wednesday', datetime.time(12), datetime.time(13))

THU_3_TO_4 = ('Thursday', datetime.time(15), datetime.time(16))

FRI_9_TO_11 = ('Friday', datetime.time(9), datetime.time(11))
FRI_12_TO_1 = ('Friday', datetime.time(12), datetime.time(13))
FRI_1_TO_2 = ('Friday', datetime.time(13), datetime.time(14))

###################################################################################################
# Sample Sections
###################################################################################################
MAT137_LEC0101 = ('LEC0101', 'Y', (MON_9_TO_11, TUE_9_TO_11, WED_9_TO_11))
MAT137_LEC0201 = ('LEC0201', 'Y', (MON_12_TO_1, WED_12_TO_1, FRI_12_TO_1))

CSC110_LEC0101 = ('LEC0101', 'F', (MON_9_TO_11, TUE_9_TO_11, WED_9_TO_11))
CSC111_LEC0301 = ('LEC0301', 'S', (MON_9_TO_11, TUE_9_TO_11, FRI_1_TO_2))

CON123_LEC0123 = ('LEC0123', 'F', (FRI_1_TO_2,))
CON123_LEC0321 = ('LEC0321', 'S', (TUE_10_TO_12, FRI_1_TO_2))

CON333_LEC1337 = ('LEC1337', 'F', (WED_9_TO_11,))
CON333_LEC2001 = ('LEC2001', 'F', (MON_9_TO_11,))

STA130_LEC0101 = ('LEC0101', 'F', (THU_3_TO_4,))

TMP000_LEC0000 = ('LEC0000', 'Y', (MON_9_TO_11,))

###################################################################################################
# Sample Courses
###################################################################################################
CSC110 = ('CSC110', 'Foundations of Computer Science I', {CSC110_LEC0101})
CSC111 = ('CSC111', 'Foundations of Computer Science II', {CSC111_LEC0301})

CON123 = ('CON123', 'Foundation Construction', {CON123_LEC0123, CON123_LEC0321})
CON333 = ('CON333', 'Advanced Brick Laying', {CON333_LEC1337, CON333_LEC2001})

MAT137 = ('MAT137', 'Calculus!', {MAT137_LEC0101, MAT137_LEC0201})

STA130 = ('STA130', 'Introduction to Statistical Reasoning',
          {STA130_LEC0101})

TMP000 = ('TMP000', 'Introduction to time travel', {TMP000_LEC0000})

###################################################################################################
# Sample Schedule
###################################################################################################
SCHEDULE_1 = {
    'CSC110': CSC110_LEC0101,
    'CSC111': CSC111_LEC0301
}

SCHEDULE_2 = {
    'CON123': CON123_LEC0123,
    'CSC111': CSC111_LEC0301,
    'CON333': CON333_LEC1337
}

SCHEDULE_3 = {
    'CSC110': CSC110_LEC0101,
    'CSC111': CSC111_LEC0301,
    'MAT137': MAT137_LEC0201,
    'CON123': CON123_LEC0321
}

# Note that this is SCHEDULE_1 but with CON123 added
SCHEDULE_4 = {
    'CSC110': CSC110_LEC0101,
    'CSC111': CSC111_LEC0301,
    'CON123': CON123_LEC0123
}

###################################################################################################
# Sample Raw Data
###################################################################################################
WED_9_TO_11_RAW = {'day': 'Wednesday', 'startTime': '09:00', 'endTime': '11:00'}
MON_9_TO_11_RAW = {'day': 'Monday', 'startTime': '09:00', 'endTime': '11:00'}
CON333_LEC1337_RAW = {'sectionCode': 'LEC1337', 'term': 'F', 'meetingTimes': [WED_9_TO_11_RAW]}
CON333_LEC2001_RAW = {'sectionCode': 'LEC2001', 'term': 'F', 'meetingTimes': [MON_9_TO_11_RAW]}
CON333_RAW = {'courseCode': 'CON333', 'courseTitle': 'Advanced Brick Laying',
              'sections': [CON333_LEC1337_RAW, CON333_LEC2001_RAW]}


###################################################################################################
# Part 3 Question 1
###################################################################################################
def test_num_sections() -> None:
    """
    Test num_sections with 1 section from CSC110
    """
    assert a2_courses.num_sections(CSC110) == 1


def test_num_lecture_hours() -> None:
    """
    Test num_lecture_hours with MAT137
    """
    assert a2_courses.num_lecture_hours(MAT137_LEC0101) == 6


###################################################################################################
# Part 3 Question 2
###################################################################################################
def test_times_conflict() -> None:
    """
        Test times_conflict with conflicting meetings times that overlap
    """
    m1 = TUE_9_TO_11
    m2 = TUE_10_TO_12
    expected = True
    actual = a2_courses.times_conflict(m1, m2)
    assert actual == expected


def test_times_no_conflict() -> None:
    """
    Test times_conflict with non-conflicting meetings times
    """
    m1 = MON_9_TO_11
    m2 = TUE_10_TO_12
    expected = False
    actual = a2_courses.times_conflict(m1, m2)
    assert actual == expected


def test_sections_conflict() -> None:
    """
    Test sections_conflict with conflicting sections
    """
    assert a2_courses.sections_conflict(CON333_LEC2001, MAT137_LEC0101)
    assert a2_courses.sections_conflict(CON123_LEC0321, CSC111_LEC0301)


def test_sections_no_conflict() -> None:
    """
    Test sections_conflict with non-conflicting sections
    """
    assert not a2_courses.sections_conflict(CON123_LEC0123, CON123_LEC0321)
    assert not a2_courses.sections_conflict(CON123_LEC0123, CSC111_LEC0301)


def test_is_valid() -> None:
    """
    Test is_valid with valid schedule
    """
    assert a2_courses.is_valid(SCHEDULE_1)
    assert a2_courses.is_valid(SCHEDULE_2)
    assert a2_courses.is_valid(SCHEDULE_4)


def test_not_valid() -> None:
    """
    Test is_valid with invalid schedule
    """
    assert not a2_courses.is_valid(SCHEDULE_3)


def test_2_possible_schedule_combinations() -> None:
    """
    Test possible_schedule_combinations with 2 possible combinations
    """
    assert len(a2_courses.possible_schedules(MAT137, CSC111)) == 2


def test_4_possible_schedule_combinations() -> None:
    """
    Test possible_schedule_combinations with 4 possible combinations
    """
    assert len(a2_courses.possible_schedules(MAT137, CON333)) == 4


def test_1_valid_schedule_combinations() -> None:
    """
    Test valid_schedule_combinations with valid schedule combination, bounds of 1
    """
    assert len(a2_courses.valid_schedules(MAT137, CSC111)) == 1


def test_4_valid_schedule_combinations() -> None:
    """
    Test valid_schedule_combinations with 4 valid schedule combinations
    """
    assert len(a2_courses.valid_schedules(CON123, CON333)) == 4


def test_possible_five_course_schedules() -> None:
    """
    Test possible_five_course_schedules with five possible course schedules
    """
    assert len(a2_courses.possible_five_course_schedules(
        CSC110, CSC111, CON123, CON333, MAT137)) == 8


def test_invalid_five_course_schedules() -> None:
    """
    Test valid_five_course_schedules with invalid five course schedule
    """
    assert not len(a2_courses.possible_five_course_schedules(
        CSC110, CSC111, CON123, CON333, TMP000)) == 0


###################################################################################################
# Part 3 Question 3
###################################################################################################
def test_section_compatible() -> None:
    """
    Test is_section_compatible with compatible sections
    """
    assert a2_courses.is_section_compatible(SCHEDULE_1, CON123_LEC0123)


def test_section_not_compatible() -> None:
    """
    Test is_section_compatible with incompatible sections
    """
    assert not a2_courses.is_section_compatible(SCHEDULE_1, TMP000_LEC0000)
    assert not a2_courses.is_section_compatible(SCHEDULE_3, CON333_LEC2001)


def test_course_compatible() -> None:
    """
    Test is_course_compatible with compatible course
    """
    assert a2_courses.is_course_compatible(SCHEDULE_1, CON123)


def test_course_not_compatible() -> None:
    """
    Test is_course_compatible with incompatible course
    """
    assert not a2_courses.is_course_compatible(SCHEDULE_1, TMP000)
    assert not a2_courses.is_course_compatible(SCHEDULE_1, CON333)


def test_compatible_sections() -> None:
    """
    Test compatible_sections with compatible sections
    """
    assert a2_courses.compatible_sections(SCHEDULE_1, CON123) == {CON123_LEC0123}


# TODO: Create more tests

###################################################################################################
# Part 4
###################################################################################################
def test_transform_course_data() -> None:
    """
    Test transform_course_data
    """
    expected = CON333
    actual = a2_part4.transform_course_data(CON333_RAW)
    assert actual == expected


def test_transform_section_data() -> None:
    """
    Test transform_section_data
    """
    expected = CON333_LEC2001
    actual = a2_part4.transform_section_data(CON333_LEC2001_RAW)
    assert actual == expected


def test_transform_meeting_time_data() -> None:
    """
    Test transform_meeting_time_data
    """
    expected = MON_9_TO_11
    actual = a2_part4.transform_meeting_time_data(MON_9_TO_11_RAW)
    assert actual == expected


# TODO: Create more tests

if __name__ == "__main__":
    pytest.main(['a2_example_tests.py'])
