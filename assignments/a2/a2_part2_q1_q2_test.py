from a2_part2_q1_q2 import mystery_1a_flat, mystery_1b_flat, mystery_2a_no_if, mystery_2b_no_if, mystery_2c_no_if
from hyhelper import *


def mystery_1a_nested(x: int, y: set[int]) -> str:
    """Mystery 1a."""
    if len(y) > 1 and x <= 0:
        return 'David'
    else:
        if x > 1 and sum({n**2 for n in y}) >= 10:
            return 'Mario'
        else:
            return 'David'


def mystery_1b_nested(n: int, rows_of_nums: list[list[int]]) -> int:
    """Mystery 1b."""
    if len(rows_of_nums) > n > 0:
        if n == 1:
            return 0
        elif n in rows_of_nums[n]:
            return sum(rows_of_nums[n]) + n
        else:
            return sum(rows_of_nums[0])
    else:
        if len(rows_of_nums) > 20:
            return 20
        else:
            return n


def mystery_2a_if(x: int, y: int, z: set[int]) -> bool:
    """Mystery 2a."""
    if x >= y:
        if x in z:
            return True
        elif y not in z:
            return False
        else:
            return False
    else:
        if x in z:
            return False
        elif y not in z:
            return True
        else:
            return False


def mystery_2b_if(n: int) -> bool:
    """Mystery 2b."""
    if n % 2 == 0:
        if n % 3 == 1:
            return True
        else:
            return False
    elif n <= 4:
        if n < 0:
            return True
        else:
            return False
    else:
        if n % 3 == 1:
            return False
        else:
            return True


def mystery_2c_if(c1: int, c2: int, c3: int) -> bool:
    """Mystery 2c."""
    if c1 == c2:
        return False
    elif c1 > c2:
        if c3 <= c2:
            return False
        else:
            return True
    else:
        if c2 < c3:
            return True
        else:
            return False


if __name__ == '__main__':
    tests = [
        (
            (mystery_1a_nested, mystery_1a_flat),
            ((-1, {1, 2}), (2, {10}), (-1, {0}))
        ),
        (
            (mystery_1b_nested, mystery_1b_flat),
            ((1, [[1], [1]]), (2, [[-999], [1], [2, 3]]), (2, [[-999, 9999], [1], [3, 4]]),
             (-1, [[1]] * 21), (-1, []))
        ),
        (
            (mystery_2a_if, mystery_2a_no_if),
            ((4, 2, {4}), (4, 2, {3}), (4, 2, {2}), (2, 4, {2}), (2, 4, {3}), (2, 4, {4}))
        ),
        (
            (mystery_2b_if, mystery_2b_no_if),
            ((4,), (2,), (-1,), (3,), (7,), (5,))
        ),
        (
            (mystery_2c_if, mystery_2c_no_if),
            ((1, 1, 0), (2, 1, 1), (2, 1, 2), (1, 2, 3), (1, 2, 1))
        )
    ]

    for funcs, paramsList in tests:
        color(f'&6Running tests for: {funcs}')
        for params in paramsList:
            color(f'* Test case {params}')
            orig = funcs[0](*params)
            flat = funcs[1](*params)
            color(f'  - Orig: &b{orig}')
            color(f'  - Flat: &b{flat}')
            assert orig == flat
            color(f'&a    Pass!')


