"""Стан окремої спроби. Перший варіант у банку — правильний."""
import random
from datetime import datetime,timezone
from time import monotonic

BANK=[
 ("Яка колекція зберігає унікальні елементи?","set","list","tuple","str"),
 ("Що створює анонімну функцію?","lambda","yield","with","pass"),
 ("Як викликати конструктор базового класу?","super().__init__()","self.base()","base.init()","parent.new()"),
 ("Який метод повертає кількість елементів для len(obj)?","__len__","__size__","__iter__","__count__"),
 ("Що поверне 7 // 2?","3","3.5","4","2"),
 ("Який модуль читає CSV?","csv","math","time","sys"),
 ("Який тип є незмінним?","tuple","list","dict","set"),
 ("Що робить yield?","Видає значення генератора","Завершує процес","Сортує список","Викликає конструктор"),
 ("Який блок виконується після try навіть при винятку?","finally","else","except KeyError","elif"),
 ("Що робить with open(...)?","Закриває файл при виході з блоку","Завжди видаляє файл","Створює каталог","Копіює файл")]

class Quiz:
    def __init__(self):
        self.questions=random.sample(BANK,len(BANK))
        self.index=self.score=0
        self.started=monotonic()
        self.options=[]

    def prompt(self):
        question,*answers=self.questions[self.index]
        self.options=random.sample(answers,len(answers))
        return f"{self.index+1}/10. {question}\n"+"\n".join(f"{i}. {v}" for i,v in enumerate(self.options,1))

    def answer(self,choice):
        if choice not in ("1","2","3","4"):
            return "Введи номер від 1 до 4."
        correct=self.questions[self.index][1]
        hit=self.options[int(choice)-1]==correct
        self.score+=hit
        self.index+=1
        feedback="Правильно!" if hit else "Правильна відповідь: "+correct
        if self.index==len(self.questions):
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            return f"{feedback}\nРезультат: {self.score}/10. {date}. Тривалість: {int(monotonic()-self.started)} с."
        return feedback+"\n"+self.prompt()
