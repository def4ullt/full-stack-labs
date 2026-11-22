"""Розширення контактів CSV з атомарною заміною після обробки всіх рядків."""
import csv
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile

class Person:
    def __init__(self,surname,first_name,birth_date,nickname=""):
        self.surname,self.first_name,self.nickname=surname,first_name,nickname
        self.birth_date=birth_date if isinstance(birth_date,date) else date.fromisoformat(birth_date.replace(" ",""))

    def get_fullname(self):
        return f"{self.surname} {self.first_name}"

    def get_age(self):
        today=date.today()
        birth=self.birth_date
        return str(today.year-birth.year-((today.month,today.day)<(birth.month,birth.day)))

def modifier(filename):
    path=Path(filename)
    with path.open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        fields=[k for k in reader.fieldnames if k not in ("fullname","age")]
        fields.insert(fields.index("name")+1,"fullname")
        fields.append("age")
        rows=list(reader)
    for row in rows:
        person=Person(row["surname"],row["name"],row["birth_date"],row.get("nickname",""))
        row.update(fullname=person.get_fullname(),age=person.get_age())
    with NamedTemporaryFile("w",dir=path.parent,delete=False,encoding="utf8",newline="") as tmp:
        writer=csv.DictWriter(tmp,fields)
        writer.writeheader()
        writer.writerows(rows)
    Path(tmp.name).replace(path)

if __name__=="__main__":
    import sys
    modifier(sys.argv[1])
