"""Тринадцять операцій. Апостроф усередині слова зберігається."""
import re
TOKEN = r"[^\W\d_]+(?:['’][^\W\d_]+)*"

def analyze(text, first, last, word):
    words = re.findall(TOKEN, text)
    letters = text.lower()
    half = len(text)//2
    names = []
    for sentence in re.split(r"[.!?]+", text):
        names.extend(w for w in re.findall(TOKEN, sentence)[1:] if w[0].isupper())
    return [
        sum(w.casefold().startswith(first.casefold()) for w in words),
        (text.replace(":", "%"), text.count(":")),
        (text.replace(".", ""), text.count(".")),
        (text.replace("а", "о"), text.count("а"), len(text)),
        letters, (text.replace("о", ""), text.count("о")),
        text[:half].replace("п", "*") + text[half:],
        sum(w.casefold() == word.casefold() for w in words),
        re.sub(TOKEN, lambda m: m[0].capitalize(), text),
        ([w for w in words if w.lower().startswith(first.lower())],
         [w for w in words if w.lower().endswith(last.lower())]),
        sum(c in "aeiou" for c in letters),
        sum(c in "bcdfghjklmnpqrstvwxyz" for c in letters), names]

if __name__ == "__main__":
    results = analyze(input("Текст: "), input("Початкова літера: "), input("Кінцева літера: "), input("Слово: "))
    for n, value in enumerate(results, 1):
        print(n, value)
