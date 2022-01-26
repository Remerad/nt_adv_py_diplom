# Функции использующие REST:
# bot.get_user_data
# vk_search.search_users_in_vk
# vk_search.get_one_user_photos_urls_list
#TODO: сделать обработку ошибок

import json
import requests
from pprint import pprint

users_params = {
    'count': 100,
    'fields': 'sex, city, bdate, relation,activities, interests, music, movies, tv, books, games',
    'age_from': 25,
    'age_to': 35
}


def get_user_data(token, user_id):
    url = 'https://api.vk.com/method/'
    users_info_url = url + 'users.get'
    users_info_params = {
        'user_ids': user_id,
        'fields': 'sex, bdate, city, relation, country'
    }
    params = {
        'access_token': token,
        'v': 5.131
    }
    response = requests.get(users_info_url, params={**params, **users_info_params})
    pprint(response.json())
    #pprint(response.json()['response'][0])
    if 'error' in response.json().keys():
        print("Опа!")
        return 0
    else:
        print(response.json()['response'][0])
        return response.json()['response'][0]

def search_users_in_vk(token, users_params_to_search):
    YA_API_BASE_URL = 'https://api.vk.com/method/'
    auth_params = {
        'access_token': token,
        'count': 100,
        'v': 5.131
    }
    response = requests.get(YA_API_BASE_URL + 'users.search',
                            params={**users_params_to_search, **auth_params})
    founded_users_ids = []
    if 'error' in response.json().keys():
        print("Опа!")
        return 0
    else:
        with open('founded_users.json', 'w', encoding='utf-8') as f:
            json.dump("Эрзац база данных найденных людей.\n", f, indent=4, ensure_ascii=False)
        with open('founded_users.json', 'a', encoding='utf-8') as f:
            json.dump(response.json()["response"]["items"], f, indent=4, ensure_ascii=False)
        return response.json()['response']["items"]


def get_one_user_photos_urls_list(token, photos_owner_id):
    #Выдает список ссылок на фото полльзователя с указанным id
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': str(photos_owner_id),
        'album_id': 'profile',
        'access_token': token,
        'extended': 1,
        'v': '5.131'
    }
    response = requests.get(URL, params=params).json()
    #pprint(response)
    user_photos_urls_list = []

    if not 'error' in response.keys():
        for photo in response['response']['items']:
            max_size = 0
            max_size_url = ''
            for photo_size in photo['sizes']:
                if photo_size['height'] >= max_size and photo_size['url'] != '':
                    max_size = photo_size['height']
                    max_size_url = photo_size['url']
            user_photos_urls_list.append({'id': photo['id'], 'likes': photo['likes']['count'], 'url': max_size_url})
    return {'owner_id': photos_owner_id,
            'items': sorted(user_photos_urls_list, key=lambda k: k['likes'], reverse=True)[:3]}
    #return response


def get_one_user_photos_urls_list(token, photos_owner_id):
    #Выдает список ссылок на фото полльзователя с указанным id
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': str(photos_owner_id),
        'album_id': 'profile',
        'access_token': token,
        'extended': 1,
        'v': '5.131'
    }
    response = requests.get(URL, params=params).json()
    #pprint(response)
    user_photos_urls_list = []

    if not 'error' in response.keys():
        for photo in response['response']['items']:
            max_size = 0
            max_size_url = ''
            for photo_size in photo['sizes']:
                if photo_size['height'] >= max_size and photo_size['url'] != '':
                    max_size = photo_size['height']
                    max_size_url = photo_size['url']
            user_photos_urls_list.append({'id': photo['id'], 'likes': photo['likes']['count'], 'url': max_size_url})
    return {'owner_id': photos_owner_id,
            'items': sorted(user_photos_urls_list, key=lambda k: k['likes'], reverse=True)[:3]}
