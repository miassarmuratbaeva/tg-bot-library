import json
import os
import requests
TOKEN = '8358759456:AAF5TaDcvHLZ20gBlh-kU9w6mKvktsmTTz8'

TG_BOT_URL = f'https://api.telegram.org/bot{TOKEN}'
def load_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json","r", encoding = "utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
def save_user(new_user):
    users = load_users()
    for user in users:
        if user["tg_id"] == new_user["tg_id"]:
            return None
    users.append(new_user)
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    
def get_updates(offset: int | None, limit: int = 100):
    url = f'{TG_BOT_URL}/getUpdates'
    params = {'offset': offset, 'limit': limit}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['result']

def send_message(chat_id: int | str, text: str, reply_markup=None):
    url = f'{TG_BOT_URL}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text
    }
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    requests.get(url, params=params)

def main():
    offset = None
    print("Bot ishlayabdi")
    while True:
        updates = get_updates(offset)
        for update in updates:
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                user = update['message']['from']
                if 'text' in update['message']:
                    text = update['message']['text']
                    if text == '/start':
                        new_user = {
                            'tg_id': user['id'],
                            'first_name': user['first_name'],
                            'last_name': user.get('last_name'),
                            'username': user.get('username')
                        }
                        saved = save_user(new_user)
                        if saved is None:
                            greeting = f"Assalamu alaykum {user['first_name']}! Qaytganingiz bilan!"
                        else:
                            greeting = f"Assalamu alaykum {user['first_name']}! Botga xush kelibsiz!"
                        keyboard = {
                            "keyboard": [
                                ["Buyurtmalarga otish"],
                                ["Mening buyurtmalarim", "Sozlamalar"],
                                ["Biz haqimizda", "Fikr qoldirish"]
                            ],
                            "resize_keyboard": True,
                            "one_time_keyboard": False
                        }
                        send_message(chat_id, greeting, reply_markup=keyboard)
                    else:
                        send_message(chat_id, f"Siz yozdingiz: {text}")
            offset = update['update_id'] + 1

main()