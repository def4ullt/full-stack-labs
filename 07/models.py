"""Три моделі предметних областей і демонстрації переходів між станами."""
import string
from collections import Counter

class Alphabet:
    lang="Ua"
    letters="абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    def __init__(self,lang=lang,letters=letters):
        self.lang,self.letters=lang,list(letters)
    def print_alphabet(self):
        print(*self.letters)
    def letters_num(self):
        return len(self.letters)
    @staticmethod
    def is_ua_lang(text):
        chars=[c for c in text.lower() if c.isalpha()]
        return bool(chars) and all(c in Alphabet.letters for c in chars)

class EngAlphabet(Alphabet):
    __en_letters_num=26
    def __init__(self):
        super().__init__("En",string.ascii_lowercase)
    def letters_num(self):
        return self.__en_letters_num
    def is_en_letter(self,text):
        return len(text)==1 and text.lower() in self.letters
    @staticmethod
    def example():
        return "Read a little every day."

class House:
    def __init__(self,area=70,price=100000):
        self._area,self._price=area,price
    def final_price(self,discount):
        if not 0<=discount<=100:
            raise ValueError("Знижка має бути від 0 до 100")
        return self._price*(100-discount)/100

class SmallHouse(House):
    def __init__(self,price=60000):
        super().__init__(40,price)

class Human:
    default_name,default_age="Анна",20
    def __init__(self,name=default_name,age=default_age,money=0,house=None):
        self.name,self.age,self.__money,self.__house=name,age,money,house
    def info(self):
        print(self.name,self.age,self.__money,self.__house._area if self.__house else "без житла")
    @staticmethod
    def default_info():
        print(Human.default_name,Human.default_age)
    def __make_deal(self,house,price):
        self.__money-=price
        self.__house=house
    def earn_money(self,amount):
        if amount<0:
            raise ValueError("Від’ємний заробіток")
        self.__money+=amount
    def buy_house(self,house,discount=10):
        price=house.final_price(discount)
        if self.__money<price:
            print("Недостатньо коштів")
            return False
        self.__make_deal(house,price)
        return True

class Apple:
    states=("Відсутнє","Цвітіння","Зелене","Червоне")
    def __init__(self,index):
        self._index,self._state=index,self.states[0]
    def grow(self):
        self._state=self.states[min(self.states.index(self._state)+1,3)]
    def is_ripe(self):
        return self._state==self.states[-1]

class AppleTree:
    def __init__(self,count):
        self.apples=[Apple(i) for i in range(count)]
    def grow_all(self):
        for apple in self.apples:
            apple.grow()
    def all_are_ripe(self):
        return bool(self.apples) and all(a.is_ripe() for a in self.apples)
    def give_away_all(self):
        self.apples.clear()

class Gardener:
    def __init__(self,name,tree):
        self.name,self._tree=name,tree
    def work(self):
        self._tree.grow_all()
    def harvest(self):
        if self._tree.all_are_ripe():
            self._tree.give_away_all()
        else:
            print("Ще немає стиглого врожаю")
    @staticmethod
    def apple_base(apples):
        print(len(apples),dict(Counter(a._state for a in apples)))

if __name__=="__main__":
    en=EngAlphabet()
    en.print_alphabet()
    print(en.letters_num(),en.is_en_letter("J"),Alphabet.is_ua_lang("Ж"),en.example())
    Human.default_info()
    buyer=Human()
    buyer.info()
    house=SmallHouse()
    buyer.buy_house(house)
    buyer.earn_money(60000)
    buyer.buy_house(house)
    buyer.info()
    tree=AppleTree(4)
    gardener=Gardener("Анна",tree)
    gardener.apple_base(tree.apples)
    gardener.work()
    gardener.harvest()
    while not tree.all_are_ripe():
        gardener.work()
    gardener.harvest()
    gardener.apple_base(tree.apples)
