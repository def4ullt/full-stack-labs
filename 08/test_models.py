"""python -m unittest discover -s 08 -v (з каталогу Labs)."""
import sys
from pathlib import Path
from unittest import TestCase,main
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"06"))
from shop import Shop,Discount
from user import User
from admin import Admin

class ShopTests(TestCase):
    def test_inventory(self):
        shop=Shop("Ліра","музика")
        self.assertEqual(shop.number_of_units,0)
        shop.set_number_of_units(2)
        shop.increment_number_of_units(3)
        self.assertEqual(shop.number_of_units,5)
        for value in (-1,1.5):
            with self.assertRaises(ValueError):
                shop.increment_number_of_units(value)
        self.assertEqual(shop.number_of_units,5)

    @patch("builtins.print")
    def test_display(self,out):
        shop=Shop("Ліра","музика")
        shop.describe_shop()
        out.assert_called_with("Ліра","музика")
        shop.open_shop()
        out.assert_called_with("Ліра","відкрито")

    @patch("builtins.print")
    def test_discount(self,out):
        shop=Discount("Ліра","музика",["струни"])
        self.assertIsInstance(shop,Shop)
        shop.get_discounts_ptoducts()
        out.assert_called_once_with("струни",sep=", ")

class UserTests(TestCase):
    def test_independent_counters(self):
        a,b=User("А","Б"),User("В","Г")
        a.increment_login_attempts()
        a.increment_login_attempts()
        self.assertEqual((a.login_attempts,b.login_attempts),(2,0))
        a.reset_login_attempts()
        self.assertEqual(a.login_attempts,0)

    @patch("builtins.print")
    def test_profile(self,out):
        u=User("Іван","Лис","user@example.org","lis",True)
        self.assertTrue(u.newsletter)
        u.describe_user()
        out.assert_called_with("Іван","Лис")
        u.greeting_user()
        out.assert_called_with("Вітаю, Іван!")

    @patch("builtins.print")
    def test_admin(self,out):
        a,b=Admin("А","Б"),Admin("В","Г")
        self.assertIsInstance(a,User)
        a.priv.privileges.append("publish")
        self.assertNotIn("publish",b.priv.privileges)
        a.priv.show_privileges()
        out.assert_called_with(*a.priv.privileges,sep="\n")

if __name__=="__main__":
    main()
