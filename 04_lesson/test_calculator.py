from calculator import Calculator

calculator = Calculator()

res = calculator.sum(4, 5)
assert res == 9

res = calculator.sum(-6, -10)
assert res == -16

res = calculator.sum(-6, 6)
assert res == 0

res = calculator.sum(5.6, 4.3)  # Python посчитает сумму
res = round(res, 1)  # округлит ее до одного знака после запятой
print(res)  # напечатает сумму
assert res == 9.9

res = calculator.sum(10, 0)
assert res == 10

res = calculator.div(10, 2)
assert res == 5

res = calculator.div(10, 0)
assert res is None
