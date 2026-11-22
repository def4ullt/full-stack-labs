from user import User

class Privileges:
    def __init__(self):
        self.privileges=["Allowed to add message","Allowed to delete users","Allowed to ban users"]

    def show_privileges(self):
        print(*self.privileges,sep="\n")

class Admin(User):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.priv=Privileges()
