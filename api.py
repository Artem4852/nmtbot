import requests, json, os, dotenv, random
from bs4 import BeautifulSoup

from helper import load_user_data, save_user_data

dotenv.load_dotenv()

os.makedirs("images", exist_ok=True)

sections = {
    "history": 4,
    "ukrainian": 36,
    "math": 2,
    "physics": 8,
    "chemistry": 9,
    "biology": 7,
    "geography": 6,
    "ukrainian_literature": 45,
    "english": 12,
}

class Loader():
    def __init__(self):
        self.url = "https://zno.osvita.ua/users/znotest/questions/"
        self.session = requests.Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        self.cookies = {
            "ost": os.getenv("ost"),
            "osuid": os.getenv("osuid"),
            "order": os.getenv("order"),
            "premium": os.getenv("premium"),
        }

        self.payload = {
            "section": None,
            "op": "questions"
        }

    def load_questions_file(self):
        with open("questions.json", "r") as file:
            return json.load(file)
    
    def save_questions_file(self, questions):
        with open("questions.json", "w") as file:
            json.dump(questions, file)

    def load_questions_api_raw(self, section):
        self.payload["section"] = sections[section]
        r = self.session.post(self.url, data=self.payload, cookies=self.cookies)
        return r.json()["questions"]
    
    def load_questions_api(self, section):
        questions = self.load_questions_api_raw(section)
        clean_questions = []
        for question in questions:
            clean_question = {
                "question": question["quest"],
                "id": question["id"],
                "img": "",
                "type": "",
                "answers1": [],
                "answers2": [],
                "result": question["result"],
                "explanation": question["explanation"]
            }

            if "img" in clean_question["question"]:
                soup = BeautifulSoup(clean_question["question"], "html.parser")
                img = soup.find("img")
                img_url = "https://zno.osvita.ua" + img["src"]
                img_r = requests.get(img_url)
                img_path = f"images/{img_url.split('/')[-3]}_{img_url.split('/')[-2]}.png"
                with open(img_path, "wb") as file:
                    file.write(img_r.content)
                clean_question["question"] = str(soup).replace(str(img), "")
                clean_question["img"] = img_path

            if question["ans1"] != "":
                print(question["ans1"])
                clean_question["type"] = "connect"
                for n in range(1, 11):
                    if question[f"ans{n}"] == "":
                        break
                    clean_question["answers1"].append(question[f"ans{n}"])
                for l in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
                    if question[f"ans{l}"] == "":
                        break
                    clean_question["answers2"].append(question[f"ans{l}"])
            else:
                clean_question["type"] = "single"
                for l in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
                    if question[f"ans{l}"] == "":
                        break
                    clean_question["answers1"].append(question[f"ans{l}"])
            clean_questions.append(clean_question)

        questions_data = self.load_questions_file()
        questions_data[section] += clean_questions
        unique_questions = {q["id"]: q for q in questions_data[section]}
        questions_data[section] = list(unique_questions.values())

        self.save_questions_file(questions_data)
        return clean_questions
    
    def random_question(self, user_id, section):
        user_data = load_user_data()
        
        if section not in user_data[user_id]:
            user_data[user_id][section] = []

        seen = user_data[user_id][section]
        questions = self.load_questions_file()[section]
        if len(seen) == len(questions):
            self.load_questions_api(section)
        questions = self.load_questions_file()[section]
        question = random.choice([q for q in questions if q["id"] not in seen])

        user_data[user_id][section].append(question["id"])
        save_user_data(user_data)
        return question
    
    def get_question(self, section, question_id):
        questions = self.load_questions_file()[section]
        question = [q for q in questions if q["id"] == question_id][0]
        return question

if __name__ == "__main__":
    loader = Loader()
    print(loader.random_question("879805663", "history"))