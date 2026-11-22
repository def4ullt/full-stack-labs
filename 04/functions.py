"""Обчислення, решето дільників і вимірювання часу без консольного виводу."""
from functools import wraps
from math import hypot, sqrt, lcm, isqrt
from random import Random
from time import perf_counter

def rectangle(a,b):
    return a*b

def inside(point, center, radius):
    return hypot(point[0]-center[0], point[1]-center[1]) < radius

def triangle(a,b,c):
    p = (a+b+c)/2
    if min(a,b,c)<=0 or max(a,b,c)>=p:
        raise ValueError("Трикутник не існує")
    return sqrt(p*(p-a)*(p-b)*(p-c))

def quadrilateral(x,y,z,t):
    return rectangle(x,y)/2 + triangle(hypot(x,y),z,t)

def divisible(n, divisors):
    step = lcm(*divisors)
    if step == 0:
        raise ValueError("Дільник не може дорівнювати нулю")
    return list(range(step,n+1,step))

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        wrapper.seconds = perf_counter()-start
        return result
    return wrapper

@timed
def odd_divisors(a,n):
    # Дільники утворюють пари. Лише у квадратів корінь утворює одну пару із собою.
    return [i*i for i in range(isqrt(max(0,a-1))+1, isqrt(n)+1)]

@timed
def primes(n,mode="list"):
    sieve = bytearray([1])*(n+1)
    for p in range(2,isqrt(n)+1):
        if sieve[p]:
            sieve[p*p::p] = bytes((n-p*p)//p+1)
    nums = [i for i in range(2,n+1) if sieve[i]]
    if mode == "count":
        return len(nums)
    return "\n".join(map(str,nums)) if mode=="column" else nums

@timed
def select(values,bottom,upper):
    if any(type(v) is not int or v<0 for v in (bottom,upper)):
        raise ValueError("Межі мають бути невід’ємними цілими.")
    lo,hi = min(values)+bottom,max(values)-upper
    if lo>hi:
        raise ValueError("Межі виходять за допустимий діапазон.")
    return [v for v in values if lo<=v<=hi]

def nums(prompt):
    return list(map(float,input(prompt+" ").split()))

if __name__=="__main__":
    for _ in range(3):
        print("Площа:",rectangle(*nums("Дві сторони прямокутника:")))
    sides = [hypot(*nums("Два катети:")) for _ in range(2)]
    print("Гіпотенузи:", sides, "менша та більша:", sorted(sides))
    a,b,r=nums("Центр a b і радіус:")
    print("Точок всередині:",sum(inside(nums("x y:"),(a,b),r) for _ in range(3)))
    print(quadrilateral(*nums("Сторони X Y Z T:")))
    print(divisible(int(input("n: ")),list(map(int,input("Дільники: ").split()))))
    a,n=map(int,input("Межі M N: ").split())
    print(odd_divisors(a,n),primes(n,input("list/column/count: ")))
    rng=Random(42)
    values=[rng.randint(1,100) for _ in range(int(input("Довжина списку: ")))]
    try:
        print(values, select(values,*map(int,input("bottom upper: ").split())))
    except (TypeError,ValueError) as error:
        print(error)
    print("N; квадрати, с; прості, с; фільтр, с")
    for k in range(1,7):
        n=10**k
        values=[rng.randrange(n)+1 for _ in range(n)]
        odd_divisors(1,n)
        primes(n,"count")
        select(values,0,0)
        print(n,odd_divisors.seconds,primes.seconds,select.seconds)
