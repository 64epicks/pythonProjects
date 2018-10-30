import numpy as np
import time
from decimal import Decimal

# Euler
# val = 0
# i = 1
# while True:
#     val += 1 / float(np.power(i, 2))
#     print(np.sqrt(val * 6))
#     i = i + 1

# Little bit faster
# def prod(num):
#     return np.math.factorial(num)
#     val = 0
#     for i in range(num + 1)[0:]:
#         val = val * i
#     return val

# k1 = Decimal(545140134)
# k2 = Decimal(13591409)
# k3 = Decimal(640320 )
# k4 = Decimal(100100025)
# k5 = Decimal(327843840)
# k6 = Decimal(53360)

# value = Decimal(0)
# n = 0
# while True:
#     value += np.power(-1, n) * ((prod(6 * n) * (k2 + (n * k1))) / (prod(np.power(prod(n), 3) * (3 * n)) * np.power(8 * k4 * k5, n)))
#     print(Decimal((k6 * np.sqrt(k3)) / value))
#     n = n + 1

