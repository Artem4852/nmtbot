import json, re

letters = ["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З"]
letters_uk_en = {
    "а": "a",
    "б": "b",
    "в": "c",
    "г": "d",
    "ґ": "e",
    "д": "f",
    "е": "g",
    "є": "h",
    "ж": "i",
    "з": "j"
}
letters_en_uk = {
    "a": "а",
    "b": "б",
    "c": "в",
    "d": "г",
    "e": "ґ",
    "f": "д",
    "g": "е",
    "h": "є",
    "i": "ж",
    "j": "з"
}
letters_en = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def load_user_data():
    with open("user_data.json", "r") as file:
        return json.load(file)

def save_user_data(user_data):
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

def fix_text(text):
    text = text.replace("<p>", "").replace("</p>", "")
    text = re.sub(r"&laquo;", "«", text)
    text = re.sub(r"&raquo;", "»", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&mdash;", "—", text)
    text = re.sub(r"&rsquo;", "’", text)
    text = re.sub(r"&ndash;", "–", text)
    text = re.sub(r"&hellip;", "...", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"<br>", "\n", text)

    text = re.sub(r"<ul>", "", text)
    text = re.sub(r"</ul>", "", text)
    text = re.sub(r"<li>", "\n• ", text)
    text = re.sub(r"</li>", "", text)
    text = re.sub(r"\r\n\r\n", "\r\n", text)
    text = re.sub(r"\r\n", "\n", text)
    return text