import requests, os, dotenv

url = "https://zno.osvita.ua/users/?do=login"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}
payload = {
    "email": "yewRNoyyJ8ti57C3VYKttKE48aPC2H@protonmail.com",
    "pass": "35hUP54QokRkpXWZlS2KRtEU%7$DoWX"
}

def update_ost():
    cookies = requests.get("https://zno.osvita.ua/users/", headers=headers).cookies

    r = requests.post(url, headers=headers, cookies=cookies, data=payload, allow_redirects=False)

    ost_value = r.cookies["ost"]
    print(ost_value)

    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_file, "ost", ost_value)
    return ost_value

if __name__ == "__main__":
    update_ost()