"""CSV без заголовка. Одна спроба на рядок, десяткові коми, тривалість у секундах."""
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
import csv
import re

@dataclass
class Attempt:
    student: str
    seconds: int
    mark: float
    answers: tuple

def read_marks(path):
    def number(s):
        return float(s.replace(",", ".")) if s != "-" else 0.0
    rows = []
    with open(path,encoding="utf-8-sig",newline="") as stream:
        for row in csv.reader(stream):
            parts = re.findall(r"(\d+)\s*(год|хв|сек)",row[3])
            seconds = sum(int(n)*{"год":3600,"хв":60,"сек":1}[u] for n,u in parts)
            rows.append(Attempt(row[0],seconds,number(row[4]),tuple(map(number,row[5:]))))
    return rows

def question_stats(rows):
    # Повна відповідь коштує 0,50. Часткові відповіді виділено окремо.
    return [(100*sum(x==0.5 for x in col)/len(col),
             100*sum(0<x<0.5 for x in col)/len(col)) for col in zip(*(r.answers for r in rows))]

def summary(rows):
    minutes = defaultdict(list)
    for row in rows:
        minutes[row.seconds//60].append(row.mark)
    lines = [f"Спроб: {len(rows)}. Студентів: {len({r.student for r in rows})}",
             f"Бал → кількість: {dict(sorted(Counter(r.mark for r in rows).items()))}",
             "Хвилина початку інтервалу → середній бал"]
    lines.extend(f"{m}: {mean(v):.2f}" for m,v in sorted(minutes.items()))
    lines.append("Питання | повна відповідь % | часткова % | нуль балів %")
    lines.extend(f"{i}: {yes:.2f} | {partial:.2f} | {100-yes-partial:.2f}"
                 for i,(yes,partial) in enumerate(question_stats(rows),1))
    lines.append("П’ять найвищих результатів за балами за хвилину")
    ranked=sorted((r for r in rows if r.seconds),key=lambda r:r.mark/r.seconds,reverse=True)
    lines.extend(f"{r.student}: {r.mark:g} / {r.seconds} с = {60*r.mark/r.seconds:.3f} бала/хв" for r in ranked[:5])
    return "\n".join(lines)

if __name__=="__main__":
    base=Path(__file__).resolve().parent
    report=summary(read_marks(base/"marks.lab6.csv"))
    print(report)
    (base/"statistics.txt").write_text(report,encoding="utf8")
