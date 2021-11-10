"""CSC110 Fall 2021 Assignment 4, Part 4: Two New Cryptosystems

Instructions (READ THIS FIRST!)
===============================
Implement each of the functions in this file. As usual, do not change any function headers
or preconditions. You do NOT need to add doctests.

You may create some additional helper functions to help break up your code into smaller parts.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 David Liu, Mario Badr, and Tom Fairgrieve.
"""


################################################################################
# Task 1 - The Grid Transpose Cryptosystem
################################################################################
def grid_encrypt(k: int, plaintext: str) -> str:
    """Encrypt the given plaintext using the grid cryptosystem.

    Preconditions:
        - k >= 1
        - len(plaintext) % k == 0
        - plaintext != ''

    >>> grid_encrypt(8, 'DAVID AND MARIO TEACH COMPUTER SCIENCE!!')
    'DDTMCA EPIVMAUEIACTNDRHEC I REAOC !N OS!'
    """
    return grid_to_ciphertext(plaintext_to_grid(k, plaintext))


def grid_decrypt(k: int, ciphertext: str) -> str:
    """Decrypt the given ciphertext using the grid cryptosystem.

    Preconditions:
        - k >= 1
        - len(ciphertext) % k == 0
        - ciphertext != ''

    >>> grid_decrypt(8, 'DDTMCA EPIVMAUEIACTNDRHEC I REAOC !N OS!')
    'DAVID AND MARIO TEACH COMPUTER SCIENCE!!'
    """
    return grid_to_plaintext(ciphertext_to_grid(k, ciphertext))


def plaintext_to_grid(k: int, plaintext: str) -> list[list[str]]:
    """Return the grid with k columns from the given plaintext.

    Preconditions:
        - k >= 1
        - len(plaintext) % k == 0
        - plaintext != ''
    """
    return [list(plaintext[i:i + k]) for i in range(0, len(plaintext), k)]


def grid_to_ciphertext(grid: list[list[str]]) -> str:
    """Return the ciphertext corresponding to the given grid.

    Preconditions:
        - grid != []
        - grid[0] != []
        - all({len(row1) == len(row2) for row1 in grid for row2 in grid})
    """
    # zip transposes an array: list(zip([1, 2], [3, 4], [5, 6])) = [(1, 3, 5), (2, 4, 6)]
    # return ''.join([s for row in zip(*grid) for s in row])
    # But since we didn't learn zip:
    return ''.join(''.join(grid[j][i] for j in range(len(grid))) for i in range(len(grid[0])))


def ciphertext_to_grid(k: int, ciphertext: str) -> list[list[str]]:
    """Return the grid corresponding to the given ciphertext.

    Note that this grid should be the one that is used to generate the ciphertext.

    Preconditions:
        - k >= 1
        - len(ciphertext) % k == 0
        - ciphertext != ''
    """
    rows = len(ciphertext) // k
    return [list(ciphertext[i:i + rows]) for i in range(0, len(ciphertext), rows)]


def grid_to_plaintext(grid: list[list[str]]) -> str:
    """Return the plaintext message corresponding to the given grid.

    Preconditions:
        - grid != []
        - grid[0] != []
        - all({len(row1) == len(row2) for row1 in grid for row2 in grid})
    """
    # They do the same thing
    return grid_to_ciphertext(grid)


################################################################################
# Task 2 - Breaking The Grid Transpose Cryptosystem
################################################################################
def grid_break(ciphertext: str, candidates: set[str]) -> set[int]:
    """Return the set of possible secret keys that decrypt the given ciphertext into a message
    that contains at least one of the candidate words.

    >>> candidate_words = {'DAVID', 'MINE'}
    >>> grid_break('DDTMCA EPIVMAUEIACTNDRHEC I REAOC !N OS!', candidate_words) == {8, 10}
    True
    """
    # For each iteration:
    # - number of rows:    rows = k
    # - number of columns: cols = floor(len / k)
    # - row index wraps around columns: row = i % rows
    # - column index:                   cols = i // rows
    #
    # Since grid[row][col] = list[row * num_cols + col],
    # The final index of a letter is (i % k * n // k + i // k)
    #
    # We first filter only possible k, then filter for messages where only the candidates exists
    c = ciphertext
    n = len(c)
    return {k for k in range(1, n) if n % k == 0
            and any(w in ''.join(c[i % k * n // k + i // k] for i in range(n)) for w in candidates)
            }


def run_example_break(ciphertext_file: str, candidates: set[str]) -> list[str]:
    """Return a list of possible plaintexts for the ciphertext found in the given file.

    Based on the A4 directory structure, you can call this function like this:
        >>> possible_plaintexts = run_example_break('ciphertexts/grid_ciphertext1.txt', {'climate'})
    """
    with open(ciphertext_file, encoding='utf-8') as f:
        ciphertext = f.read()

    return [grid_decrypt(k, ciphertext) for k in grid_break(ciphertext, candidates)]


################################################################################
# Task 3 - The Permuted Grid Transpose Cryptosystem
################################################################################
def transpose(grid: list[list[str]]) -> list[list[str]]:
    """Transpose a grid

    Preconditions:
        - grid != []
        - grid[0] != []
        - all({len(row1) == len(row2) for row1 in grid for row2 in grid})
    """
    return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]


def permutation_grid_encrypt(k: int, perm: list[int], plaintext: str) -> str:
    """Encrypt the given plaintext using the grid cryptosystem.

    Preconditions:
        - k >= 1
        - len(plaintext) % k == 0
        - sorted(perm) == list(range(0, k))
        - plaintext != ''

    >>> permutation_grid_encrypt(8, [0, 1, 2, 3, 4, 5, 6, 7],
    ...                          'DAVID AND MARIO TEACH COMPUTER SCIENCE!!')
    'DDTMCA EPIVMAUEIACTNDRHEC I REAOC !N OS!'
    >>> permutation_grid_encrypt(8, [3, 2, 5, 0, 7, 1, 6, 4],
    ...                          'DAVID AND MARIO TEACH COMPUTER SCIENCE!!')
    'IACTNVMAUE I REDDTMCN OS!A EPIAOC !DRHEC'
    """
    # Create and transpose grid
    grid = transpose([list(plaintext[i:i + k]) for i in range(0, len(plaintext), k)])
    # Permute grid
    grid = [grid[i] for i in perm]
    # Stringify
    return ''.join(s for row in grid for s in row)


def permutation_grid_decrypt(k: int, perm: list[int], ciphertext: str) -> str:
    """Return the grid corresponding to the given ciphertext.

    Note that this grid should be the one that is used to generate the ciphertext.

    Preconditions:
        - k >= 1
        - len(ciphertext) % k == 0
        - sorted(perm) == list(range(0, k))
        - ciphertext != ''

    >>> permutation_grid_decrypt(8, [0, 1, 2, 3, 4, 5, 6, 7],
    ...                          'DDTMCA EPIVMAUEIACTNDRHEC I REAOC !N OS!')
    'DAVID AND MARIO TEACH COMPUTER SCIENCE!!'
    >>> permutation_grid_decrypt(8, [3, 2, 5, 0, 7, 1, 6, 4],
    ...                          'IACTNVMAUE I REDDTMCN OS!A EPIAOC !DRHEC')
    'DAVID AND MARIO TEACH COMPUTER SCIENCE!!'
    """
    n = len(ciphertext)
    # Create grid
    grid = [list(ciphertext[i:i + n // k]) for i in range(0, len(ciphertext), n // k)]
    # Permute back
    grid = [grid[perm.index(p)] for p in range(k)]
    # Stringify transposed grid
    return ''.join(s for row in transpose(grid) for s in row)


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts'],
        'allowed-io': ['run_example_break'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
