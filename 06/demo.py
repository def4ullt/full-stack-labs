from objects import Bank,Coin,Car,Dog,Collie,Labrador,Pets,Buffer,validate_name,ShortNameError,DecimalToRoman,RomanToDecimal
from shop import Shop,Discount
from user import User
from admin import Admin

bank=Bank(100)
bank.deposit(50)
bank.withdraw(20)
print(bank.balance())
coin=Coin()
print([coin.toss() for _ in range(int(input("Кількість підкидань: ")))])
car=Car("Mitsubishi","Lancer",2010)
for action in (car.accelerate,car.brake):
    for _ in range(5):
        action()
        print(car.get_speed())
for dog in Pets(Dog("Рекс",2),Collie("Луна",3),Labrador("Макс",5)).pets:
    dog.describe()
buffer=Buffer()
buffer.add(1,2,3)
buffer.add(*range(4,13))
print(buffer.get_current_part())
try:
    validate_name(input("Ім’я: "))
except ShortNameError as error:
    print(error)
print(DecimalToRoman.convert(44),RomanToDecimal.convert("XLIV"))
store=Shop("Папір","канцелярія")
print(store.shop_name,store.store_type)
store.open_shop()
all_store=Shop("Струни","музика")
for item in (store,all_store,Shop("Зерно","кава")):
    item.describe_shop()
print(store.number_of_units)
store.number_of_units=3
print(store.number_of_units)
store.set_number_of_units(8)
store.increment_number_of_units(2)
print(store.number_of_units)
store_discount=Discount("Чай","напої",["улун"])
store_discount.get_discounts_ptoducts()
for user in (User("Марія","Коваль"),User("Іван","Лісовий")):
    user.describe_user()
    user.greeting_user()
    for _ in range(3):
        user.increment_login_attempts()
    print(user.login_attempts)
    user.reset_login_attempts()
    print(user.login_attempts)
admin=Admin("Анна","Лис")
admin.priv.show_privileges()
