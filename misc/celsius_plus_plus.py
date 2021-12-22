import math

import numpy as np
from matplotlib import pyplot as plt


# def convert_from_c(c: int):
#     k = c + 273.15
#     assert k >= 0
#
#     scale = [273.15, 0, 37, 100]
#     mapping = [273.15, 0, 50, 100]
#
#     i_scale = [scale[i + 1] - scale[i] for i in range(len(scale) - 1)]
#     i_mapping = [mapping[i + 1] - mapping[i] for i in range(len(mapping) - 1)]
#
#     s_scale = []
#     for s in scale:
#         s_scale.append(s + 0 if len(s_scale) == 0 else s_scale[-1])
#     s_mapping = []
#     for m in mapping:
#         s_mapping.append(m + 0 if len(s_mapping) == 0 else s_mapping[-1])
#
#     # 分不同部分单独 scale
#     temp = []
#     for d in s_scale:
#         temp.append(min(d, max(k, 0)))
#         k -= d
#
#     s = 0
#     for i in range(len(scale) - 1):
#         s += temp[i] / i_scale[i] * i_mapping[i]
#     s += temp[-1]
#     s -= 273.15
#     return s


def piecewise(c: int):
    if c < 0:
        return c
    if c < 37:
        return c / 37 * 50
    if c < 100:
        return 50 + (c - 37) / (100 - 37) * (100 - 50)
    return 100 + (c - 100)


def plot_eq(f, lower, upper, step=0.1):
    x_p = list(np.arange(lower, upper, step=step))
    y_p = [f(x) for x in x_p]
    plt.plot(x_p, y_p, color='#ffcccc')


if __name__ == '__main__':
    xt = [-273.15, 0, 37, 100, 200]
    yt = [-273.15, 0, 50, 100, 200]
    plt.xticks(xt)
    plt.yticks(yt)
    for x in xt:
        plt.axvline(x, color='lightgray')
    for y in yt:
        plt.axhline(y, color='lightgray')
    plot_eq(piecewise, -273.15, 200)

    # plot_eq(lambda x: 201.8125 + (-201.8125) / (1 + (x / 101.6479) ** 1.098977), -237.15, 200)
    # plot_eq(lambda x: 381.2003 * math.e ** (-(x - 407.029) ** 2/(2 * 163.9733 ** 2)), 0, 200 + 273.15)
    # plot_eq(lambda x: -437.3297 + 3.773026 * x - 0.004290584 * x ** 2, 0, 200 + 273.15)
    # plot_eq(lambda x: 3229.053 - 31.29614*x + 0.1066366*x ** 2 - 0.0001159774*x ** 3, 0, 200 + 273.15)
    # plt.xticks([x + 273.15 for x in xt], [str(x) for x in xt])
    # plt.yticks([x + 273.15 for x in yt], [str(x) for x in yt])

    plt.ylabel("°C++ (Degrees Celsius++)")
    plt.xlabel("°C (Degrees Celsius)")
    plt.show()
    # convert_from_c(10)
