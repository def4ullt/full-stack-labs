"""Зайнятість аудиторій за двотижневим розкладом кафедри КН."""
import argparse
import json
import re
import subprocess
import os
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
PAGE = "https://kkn.chnu.edu.ua/for_student/class-schedule/"
# Аудиторії з ПК або ноутбуками за описом матеріальної бази кафедри.
COMPUTER_ROOMS = "8-101 8-103 8-111 8-112 8-114 8-202 8-207 8-209".split()
ROOM = re.compile(r"(\d+)[–−-](\d+[а-яА-Яa-zA-Z]?)")
DAYS = {"понеділок", "вівторок", "середа", "четвер", "п'ятниця"}


class WorkbookLinks(HTMLParser):
    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href") or ""
        if tag == "a" and urlsplit(href).path.lower().endswith((".xls", ".xlsx")):
            print(urljoin(PAGE, href))


def analyse(rows, group):
    occupied, selected = defaultdict(set), defaultdict(set)
    slots = set()
    columns = []
    day = ""
    for i, row in enumerate(rows):
        if row[0].strip().lower() == "підгрупи":
            columns = [c for c, name in enumerate(row[4:-3], 4) if name.strip()]
            group_columns = [c for c in columns if re.match(re.escape(group) + r"(?:\(|\s|$)", row[c].strip())]
            day = ""
        label = row[0].strip().lower().replace("’", "'")
        if label in DAYS:
            day = label
        if not (day and columns and row[1].strip().isdigit() and "1-й" in row[2]):
            continue
        period = int(row[1])
        slots.update((day, period, week) for week in (1, 2))
        if i + 5 >= len(rows) or "2-й" not in rows[i + 3][2]:
            raise ValueError(f"Невідомий формат пари у рядку {i + 1}")
        for col in columns:
            # У блоці з 6 рядків аудиторія на 3-му/6-му стосується
            # окремого тижня, а на 5-му — заняття в обидва тижні.
            for offset, weeks in [(2, (1,)), (4, (1, 2)), (5, (2,))]:
                cell = rows[i + offset][col].strip()
                match = ROOM.fullmatch(cell)
                if match:
                    room = "-".join(match.groups())
                    times = {(day, period, w) for w in weeks}
                    occupied[room].update(times)
                    if col in group_columns:
                        selected[room].update(times)
    if not slots:
        raise ValueError("Не розпізнано двотижневу сітку розкладу")
    return slots, occupied, selected


def ranking(title, counts):
    print(title)
    for room, count in sorted(counts.items(), key=lambda entry: (-entry[1], entry[0])):
        print(f"  {room:8} {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, nargs="?", default=HERE / "schedule.xls")
    parser.add_argument("--group", default="444", help="Номер потоку в заголовку підгруп")
    parser.add_argument("--links", action="store_true", help="Знайти файли розкладу на сайті")
    args = parser.parse_args()
    if args.links:
        with urlopen(PAGE, timeout=20) as response:
            WorkbookLinks().feed(response.read().decode("utf-8"))
    else:
        shell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
        reader = (HERE / "read_sheet.ps1").read_text(encoding="utf-8-sig")
        env = dict(os.environ, SCHEDULE_FILE=str(args.file.resolve()))
        raw = subprocess.check_output(
            [str(shell), "-NoProfile", "-NonInteractive", "-Command",
             "& {\n" + reader + "\n} -Path $env:SCHEDULE_FILE"],
            env=env, encoding="utf8")
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
        slots, used, group_used = analyse(rows, args.group)
        print(f"Кількість пар у двотижневій сітці: {len(slots)}")
        ranking("Корпус 8 — зайняті пари", {r: len(s) for r, s in used.items() if r.startswith("8-")})
        ranking("Аудиторії з технікою — пари без запису кафедри", {r: len(slots - used[r]) for r in COMPUTER_ROOMS})
        ranking(f"Потік {args.group} — зайняті пари за аудиторіями", {r: len(s) for r, s in group_used.items()})



