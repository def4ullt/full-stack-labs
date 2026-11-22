import re
from html import unescape

def clean_review(text):
    return " ".join(re.sub(r"<[^>]+>"," ",unescape(text)).casefold().split())
