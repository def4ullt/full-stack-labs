"""Частина 1. Кожен результат залишається у списку для наступної операції."""
a = int(input("Ціле a: "))
b = int(input("Цілий ненульовий дільник b: "))
c = float(input("Дробове c: "))
d = float(input("Дробове d: "))
if b == 0:
    raise SystemExit("Дільник має бути ненульовим.")
values = [a + c, b - d, c * d, a / b, a ** b, a // b, a % b]
print("Результати:", values, "Кількість:", len(values))
print("Парні значення:", [x for x in values if x % 2 == 0])
print("На парних позиціях:", values[1::2])
values[1], values[4] = values[4], values[1]
print(values)
name = input("Прізвище та ім’я: ")
print("Роботу виконав(ла)", name)
print("Список зберігає результати різних операцій у порядку додавання.")
