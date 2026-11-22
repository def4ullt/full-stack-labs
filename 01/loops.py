"""Частина 2. Оберіть номер завдання та введіть його аргументи."""
import calendar
import math
from itertools import count

def solve(task, x):
    if task == 1:
        return [v for v in x if 1 <= v <= 3]
    if task == 2:
        return 365 + calendar.isleap(x[0])
    if task == 3:
        price = x[0]
        return round(price * (0.95 if price > 1000 else 0.97 if price > 500 else 1), 2)
    if task == 4:
        return math.cos(min(x))
    if task == 5:
        return math.sin(max(x))
    if task == 6:
        area = math.prod(x) / 2
        return (area, area / 2 if area % 2 == 0 else "Не можу ділити на 2!")
    if task == 7:
        return "January February March April May June July August September October November December".split()[x[0]-1]
    if task == 8:
        return sum(v > 0 for v in x)
    if task in (9, 10, 11, 13):
        start = x[0]
        end = 200 if task == 11 else 50 if task == 13 else x[1]
        total = 0
        for v in range(start, end + 1):
            total += v*v if task in (10, 13) else v
        return total / (end-start+1) if task == 11 else total
    if task == 12:
        a, b = x
        total = 0
        while a <= b:
            total += a
            a += 1
        return total
    if task == 14:
        k = 0
        while 5**k <= x[0]:
            k += 1
        return k
    if task == 15:
        for k in count(1):
            if k*k > x[0]:
                return k*k
    # У друкованому ряді перший член 1, наступні 5, 10, 17...
    value, k = 1, 1
    while value <= x[0]:
        k += 1
        value = k*k + 1
    return value

if __name__ == "__main__":
    prompts = ["три цілих", "рік", "ціна", "чотири числа", "три числа", "основа і висота", "місяць 1–12", "три числа", "A B", "A B", "a ≤ 200", "a b", "a від 0 до 50", "N > 1", "n", "n"]
    task = int(input("Номер вправи 1–16: "))
    if not 1 <= task <= 16:
        raise SystemExit("Невідоме завдання")
    parse = float if 3 <= task <= 6 or task == 8 else int
    print(solve(task, list(map(parse, input(prompts[task-1] + ": ").split()))))
