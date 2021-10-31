"""CSC110 Fall 2021 Assignment 3: Part 4 (Student Test Suite)

Instructions (READ THIS FIRST!)
===============================
Complete the unit tests in this file based on their docstring descriptions.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Mario Badr and Tom Fairgrieve.
"""
import pytest

from a3_part4 import load_data
from a3_ffwi_system import WeatherMetrics, FfwiOutput

import a3_ffwi_system as ffwi


class TestCalculateMr:
    """A collection of unit tests for calculate_mr."""

    def test_equation_3a_branch(self) -> None:
        """Test the branch calculate_mr that contains Equation 3a."""
        assert 123.823 == pytest.approx(ffwi.calculate_mr(2.4, 80))

    def test_equation_3b_branch(self) -> None:
        """Test the branch calculate_mr that contains Equation 3b."""
        assert 182.803 == pytest.approx(ffwi.calculate_mr(2.4, 155))


class TestCalculateM:
    """A collection of unit tests for calculate_m."""

    def test_no_mutation_mo_equals_ed(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo == ed."""
        wm_old = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        wm_new = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        ffwi.calculate_m(wm_new, 0.5, 0.5)
        assert wm_old == wm_new

    def test_no_mutation_mo_leq_ew(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo <= ew."""
        wm_old = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        wm_new = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        ffwi.calculate_m(wm_new, 0.5, 0.1)
        assert wm_old == wm_new

    def test_no_mutation_mo_greater_than_ew(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo > ew."""
        wm_old = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        wm_new = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        ffwi.calculate_m(wm_new, 5.0, 3.0)
        assert wm_old == wm_new

    def test_no_mutation_mo_greater_than_ed(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo > ed."""
        wm_old = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        wm_new = WeatherMetrics(1, 2, 3.0, 4.0, 5.0, 6.0)
        ffwi.calculate_m(wm_new, 0.01, 0.1)
        assert wm_old == wm_new


@pytest.fixture
def sample_data() -> tuple[list[WeatherMetrics], list[FfwiOutput]]:
    """A pytest fixture containing the data in data/ffwi/sample_data.csv

    NOTE: Do not change this function. Do not call this function directly. It is a pytest fixture,
    so pytest will call it automatically and pass it to test_ffmc_against_ground_truth below.
    """
    return load_data('data/ffwi/sample_data.csv')


def test_ffmc_against_ground_truth(sample_data) -> None:
    """Test the correctness of calculate_ffmc, calculate_dmc, calculate_dc, calculate_isi,
     calculate_bui, and calculate_fwi based on sample_data.

    Ensure that, for every WeatherMetric element in inputs passed to each of the calculate_
    functions mentioned above, the return value, rounded to the nearest decimal, matches the
    corresponding value from the FfwiOutput element in outputs.

    Hints:
        - You will need to use the built-in function round.
        - You may want to use pytest.approx since you are comparing float values.
    """
    ffmc = ffwi.INITIAL_FFMC
    dmc = ffwi.INITIAL_DMC
    dc = ffwi.INITIAL_DC

    inputs, outputs = sample_data
    for i in range(len(sample_data)):
        ffmc = ffwi.calculate_ffmc(inputs[i], ffmc)
        dmc = ffwi.calculate_dmc(inputs[i], dmc)
        dc = ffwi.calculate_dc(inputs[i], dc)
        isi = ffwi.calculate_isi(inputs[i], ffmc)
        bui = ffwi.calculate_bui(dmc, dc)
        fwi = ffwi.calculate_fwi(isi, bui)

        assert round(ffmc, 1) == pytest.approx(outputs[i].ffmc)
        assert round(dmc, 1) == pytest.approx(outputs[i].dmc)
        assert round(dc, 1) == pytest.approx(outputs[i].dc)
        assert round(isi, 1)== pytest.approx(outputs[i].isi)
        assert round(bui, 1) == pytest.approx(outputs[i].bui)
        assert round(fwi, 1) == pytest.approx(outputs[i].fwi)


if __name__ == '__main__':
    pytest.main(['a3_part4_tests.py'])

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'allowed-io': ['load_data'],
        'extra-imports': ['a3_ffwi_system', 'a3_part4', 'pytest'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        'disable': ['R1705', 'R0201', 'C0103', 'W0621', 'E9970'],
    })
