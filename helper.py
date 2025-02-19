import json, re, os
from PIL import Image

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

subjects_uk_en = {
    "українська_мова": "ukrainian",
    "математика": "math",
    "фізика": "physics",
    "хімія": "chemistry",
    "біологія": "biology",
    "географія": "geography",
    "українська_література": "ukrainianliterature",
    "англійська": "english",
    "історія_україни": "history",
}

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

def merge_images(paths):
    images = [Image.open(path) for path in paths]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    os.makedirs("temp", exist_ok=True)
    filename = f"temp/merged_image_{paths[0].split('/')[-1]}.jpg"
    new_image.save(filename)

    return filename