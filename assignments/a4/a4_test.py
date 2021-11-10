import math

import numpy as np
from matplotlib import pyplot as plt

from assignments.a4.a4_part2 import starting_coprime_numbers


def plot_eq(f, lower, upper, step=0.1):
    x_p = list(np.arange(lower, upper, step=step))
    y_p = [f(x) for x in x_p]
    plt.plot(x_p, y_p, color='#ffcccc')


# Initialize a list
primes = []
for possiblePrime in range(2, 1000):

    # Assume number is prime until shown it is not.
    isPrime = True
    for num in range(2, possiblePrime):
        if possiblePrime % num == 0:
            isPrime = False

    if isPrime:
        primes.append(possiblePrime)


def coprime_to_all(primes: set[int], n: int) -> int:
    """Return the positive integers less than n that are coprime to every number in primes.

    Preconditions:
        - primes != set()
        - every element of primes is prime
        - n >= math.prod(primes)
    """
    m = math.prod(primes)
    nums_so_far = starting_coprime_numbers(primes)
    phi = len(nums_so_far)
    count = 0
    while nums_so_far[-phi] + m < n:
        next_number = nums_so_far[-phi] + m
        list.append(nums_so_far, next_number)
        count += 1

    # print('m =', m)
    # print('phi(m) =', phi)
    # print('n * phi(m) / m =', n * phi / m)
    # print('n * phi(m) / m - phi(m) =', n * phi / m - phi)
    # print('count =', count)

    return count


if __name__ == '__main__':
    x = primes
    plt.plot(x, [coprime_to_all({a}, 2000) for a in x], label='count')
    plt.plot(x, [2000 - a for a in x], label='count')

    plt.ylabel('loop count')
    plt.xlabel('m')
    plt.show()
