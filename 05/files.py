"""Запуск: python files.py 1 ... 6. Для №2 числа передаються після номера."""
from collections import Counter
from datetime import datetime
from pathlib import Path
from time import perf_counter
import re
import sys

BASE=Path(__file__).resolve().parent
def stamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def run(task,args):
    if task==1:
        result=sum(map(int,(BASE/"numbers.txt").read_text().split()))
        print(result)
        (BASE/"sum_numbers.txt").write_text(str(result))
    elif task==2:
        numbers=list(map(int,args or input("Цілі числа: ").split()))
        (BASE/"parity.txt").write_text("\n".join(f"{x} — {'непарне' if x%2 else 'парне'}" for x in numbers),encoding="utf8")
    elif task in (3,4):
        with (BASE/"learning_python.txt").open(encoding="utf8") as stream:
            lines=[line.rstrip() for line in stream]
        if task==3:
            print(*lines,sep="\n")
            print(*sorted(lines,key=len,reverse=True),sep="\n")
        else:
            folder=BASE/"translated"
            folder.mkdir(exist_ok=True)
            path=folder/"C.txt"
            path.write_text("\n".join(s.replace("Python","C") for s in lines),encoding="utf8")
            true,false=[],[]
            for line in path.read_text(encoding="utf8").splitlines():
                answer=input(line+" [т/н] ").strip().lower()
                while answer not in ("т","н"):
                    answer=input("Введіть т або н: ").strip().lower()
                (true if answer=="т" else false).append(line)
            path.write_text("\n".join(true),encoding="utf8")
            (folder/"false.txt").write_text("\n".join(false),encoding="utf8")
    elif task==5:
        path=BASE/"guest_book.txt"
        lines=path.read_text(encoding="utf8").splitlines() if path.exists() else []
        if not lines:
            lines=["Створено "+stamp(),""]
        while name:=input("Ім’я (Enter — вихід): ").strip():
            message=f"{stamp()} Вітаємо, {name}!"
            print(message)
            lines.append(message)
            lines[1]="Оновлено "+stamp()
            path.write_text("\n".join(lines)+"\n",encoding="utf8")
    elif task==6:
        path=BASE/"frequencies.txt"
        created=not path.exists()
        start=perf_counter()
        text=(BASE/"article.txt").read_text(encoding="utf8").lower()
        words=Counter(re.findall(r"[a-z]+(?:'[a-z]+)?",text))
        letters=Counter(c for c in text if "a"<=c<="z")
        query=input("Слово або літера: ").strip().lower()
        seconds=perf_counter()-start
        line=f"{stamp()} | {query} | {(letters if len(query)==1 else words)[query]} | {seconds:.6f} с"
        print(line)
        with path.open("a",encoding="utf8") as f:
            if created:
                print("Створено",stamp(),file=f)
            print(line,file=f)
if __name__=="__main__":
    run(int(sys.argv[1]),sys.argv[2:])
