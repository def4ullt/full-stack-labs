class Shop:
    def __init__(self,shop_name,store_type):
        self.shop_name,self.store_type=shop_name,store_type
        self.number_of_units=0

    def describe_shop(self):
        print(self.shop_name,self.store_type)

    def open_shop(self):
        print(self.shop_name,"відкрито")

    def set_number_of_units(self,n):
        if type(n) is not int or n<0:
            raise ValueError("Потрібна невід’ємна ціла кількість.")
        self.number_of_units=n

    def increment_number_of_units(self,n):
        if type(n) is not int or n<0:
            raise ValueError("Приріст має бути цілим і невід’ємним.")
        self.set_number_of_units(self.number_of_units+n)

class Discount(Shop):
    def __init__(self,name,kind,products):
        super().__init__(name,kind)
        self.discount_products=list(products)

    def get_discounts_ptoducts(self):
        print(*self.discount_products,sep=", ")
