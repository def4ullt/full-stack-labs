"""Приватні атрибути, наслідування, винятки та буфер з обмеженою пам'яттю."""
import random

class Bank:
    def __init__(self,balance=0):
        self.__balance=0
        self.deposit(balance)

    def deposit(self,amount):
        if amount<0:
            raise ValueError("Від’ємна сума")
        self.__balance+=amount

    def withdraw(self,amount):
        if not 0<=amount<=self.__balance:
            raise ValueError("Некоректна сума зняття")
        self.__balance-=amount

    def balance(self):
        return self.__balance

class Coin:
    def __init__(self):
        self.toss()

    def toss(self):
        self.__sideup=random.choice(("heads","tails"))
        return self.__sideup

class Car:
    def __init__(self,make,model,year):
        self.make,self.model,self.year=make,model,year
        self.speed=0

    def accelerate(self):
        self.speed+=5

    def brake(self):
        self.speed=max(0,self.speed-5)

    def get_speed(self):
        return self.speed

class Dog:
    mammal,nature,breed=True,"товариський","метис"
    def __init__(self,name,age):
        self.name,self.age=name,age

    def describe(self):
        print(self.name,self.age,self.breed,self.nature)

class Collie(Dog):
    nature,breed="уважний","колі"
    def herd(self):
        return "Збирає отару"

class Labrador(Dog):
    nature,breed="грайливий","лабрадор"
    def retrieve(self):
        return "Приносить м’яч"

class Pets:
    def __init__(self,*pets):
        self.pets=list(pets)

class Buffer:
    def __init__(self):
        self.part=[]

    def add(self,*values):
        for value in values:
            self.part.append(value)
            if len(self.part)==5:
                print(sum(self.part))
                self.part.clear()

    def get_current_part(self):
        return self.part.copy()

class ShortNameError(ValueError):
    pass

def validate_name(name):
    if len(name)<10:
        raise ShortNameError("Ім’я має містити щонайменше 10 символів.")

class DecimalToRoman:
    digits=((1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I"))
    @classmethod
    def convert(cls,number):
        if not 1<=number<=3999:
            raise ValueError("Діапазон 1–3999")
        result=""
        for value,symbol in cls.digits:
            times,number=divmod(number,value)
            result+=symbol*times
        return result

class RomanToDecimal:
    @staticmethod
    def convert(text):
        original=text=text.upper()
        number=0
        for value,symbol in DecimalToRoman.digits:
            while text.startswith(symbol):
                number+=value
                text=text[len(symbol):]
        if text or DecimalToRoman.convert(number)!=original:
            raise ValueError("Неканонічний римський запис")
        return number
