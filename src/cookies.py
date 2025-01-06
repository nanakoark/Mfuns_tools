from urllib.parse import unquote
import json
from file_store import getPath

ec = '%7B%22login%22%3Atrue%2C%22user%22%3A%7B%22created_at%22%3A1620134249%2C%22state%22%3A1%2C%22avatar%22%3A%22%2Fstatic%2F8362d6bbe475d0707f1c4c41e96a8bbd5fb4614adb5bf866b2eedb31ebbe26f1.png%22%2C%22name%22%3A%22%E6%BF%91%E4%BA%9A%E5%AD%90_izNyaku%22%2C%22id%22%3A6614%2C%22updated_at%22%3A1707660039%2C%22bio%22%3A%22%E2%99%A1%20(%E0%A5%82%CB%83o%CB%82%20%E0%A5%82)%E2%81%BC%C2%B3%E2%82%8C%E2%82%83%22%2C%22gender%22%3A1%2C%22exp%22%3A4611%2C%22level_id%22%3A7%2C%22level_badge%22%3A7%2C%22badges%22%3A%5B12%5D%2C%22neko_coin%22%3A1694%2C%22follow%22%3A%7B%22follow%22%3A63%2C%22fans%22%3A74%7D%2C%22premium%22%3A%7B%7D%2C%22name_color%22%3A%22%22%2C%22banner_image%22%3A%22%2Fstatic%2Fbc477e2a3546adaa8ff00bde8d91c91e614de158dbfc8b52a650ac5f13e591f0.jpeg%22%2C%22user_auth%22%3Anull%7D%7D'

a = unquote(ec)
data = json.loads(a)
print(data['user']['id'])

with open(f'{getPath(['data','userinfo','cookies.json'])}','w',encoding='UTF8') as cookies_json:
    json.dump(data,cookies_json,ensure_ascii=False,indent=4)