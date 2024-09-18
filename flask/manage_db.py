from sympy import symbols, sqrt, pi, integrate

# 定义变量
x, a = symbols('x a')

# 定义被积函数，分别是 sqrt(2ax - x^2) 和 x 的差
integrand = sqrt(2*a*x - x**2) - x

# 计算积分
area_desired = 2 * integrate(integrand, (x, 0, a))

# 半圆的总面积
total_area = (1/2) * pi * a**2

# 计算概率
probability = area_desired / total_area

area_desired, probability.simplify()

print(probability.simplify())
