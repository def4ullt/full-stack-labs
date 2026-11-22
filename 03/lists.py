"""Зрізи, розбиття на групи і сортування за обчислюваним ключем."""
import random

def analyze(values, rng):
    twenty = [rng.randint(-100, 100) for _ in range(20)]
    whole = [rng.randint(-100, 100) for _ in range(30)]
    mixed = [rng.randint(-100, 100) if i % 2 else round(rng.uniform(-100, 100), 2) for i in range(30)]
    ten = whole[:10]
    chunks = [mixed[i:i+3] for i in range(0, 30, 3)]
    return [ (max(values), values[::-1]),
             ([x for x in values if x > 0], [x for x in values if x <= 0]),
             (twenty, sum(twenty[1::2])),
             (whole, max(whole), whole.index(max(whole))+1, sorted((x for x in whole if x%2), reverse=True) or "Непарних немає"),
             [(a,b) for a,b in zip(whole, whole[1:]) if max(a,b)<0],
             (ten, max(ten), sorted((x*x for x in ten if x<max(ten)), reverse=True)),
             (min(mixed,key=abs), sorted(mixed)),
             sorted(chunks, key=lambda group: sum(map(abs,group))) ]

if __name__ == "__main__":
    values = list(map(int, input("Введіть цілі числа через пробіл: ").split()))
    if not values:
        raise SystemExit("Потрібен хоча б один елемент.")
    for i,result in enumerate(analyze(values,random.Random()),1):
        print(i,result)
