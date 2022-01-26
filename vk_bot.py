# -*- coding: utf-8 -*-
import os
from pprint import pprint
from random import random, randint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
from dateutil.relativedelta import relativedelta #pip install python-dateutil

from DataBase_proc import DataBaseСlerk
from vk_rest_api import get_user_data, search_users_in_vk


class VKBot:
    user_data_list = []  # пока один ищущий, в перспективе - много

    def get_full_years(self, str_bdata):
        first_str = str_bdata.split(".")
        first = dt.datetime(int(first_str[2]), int(first_str[1]), int(first_str[0]))
        return relativedelta(dt1=dt.datetime.now(), dt2=first).years

    def male_female_or_none(self, sex):
        if sex == 1:
            return "женский"
        elif sex == 1:
            return "мужской"
        else:
            return "не указан"

    def __init__(self, vk_group_token):
        self.token = vk_group_token
        self.vk_session = vk_api.VkApi(token=self.token)

    def write_msg(self, user_id, message):
        vk = self.vk_session.get_api()
        vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=randint(1, 10 ** 7)
        )

    def hello_message(self, user_data):
        self.write_msg(
            user_id=user_data["id"],
            message=f'Итак, что мы знаем:'
                    f'\nВаш user_id: {user_data["id"]}'
                    f'\nВам полных лет: {self.get_full_years(user_data["bdate"])} '
                    f'\nВаш пол: {self.male_female_or_none(user_data["sex"])}'
                    f'\nВаш город: {user_data["city"]["title"]}'
        )

    def get_params_for_search(self, dict_of_client_params):
        # Данная функция делает массив данных для поиска в ВК на основе данных цели
        keys_list = dict_of_client_params.keys()
        dict_of_targets_params = {}
        if "sex" in keys_list:
            if dict_of_client_params["sex"] == 1:
                dict_of_targets_params.update({"sex": 2})
            elif dict_of_client_params["sex"] == 2:
                dict_of_targets_params.update({"sex": 1})
        if "bdate" in keys_list:
            dict_of_targets_params.update({'age_from': self.get_full_years(dict_of_client_params["bdate"]) - 5,
                                           'age_to': self.get_full_years(dict_of_client_params["bdate"]) + 5
                                           })
        if "city" in keys_list:
            dict_of_targets_params.update({'city': dict_of_client_params["city"]["id"]})
        dict_of_targets_params.update({'count': 10, 'fields': 'bdate, relation'})
        print("Параметры для поиска:")
        pprint(dict_of_targets_params)
        return dict_of_targets_params

    def make_target_params_str(self, dict_of_targets_params):
        if dict_of_targets_params == None:
            return 0
        res_str = "Человека с какими параметрами ищем:"
        if "sex" in dict_of_targets_params.keys():
            if dict_of_targets_params["sex"] == 1:
                res_str += "\nженского пола"
            elif dict_of_targets_params["sex"] == 2:
                res_str += "\nмужского пола"
        else:
            res_str += "\nпол не важен"
        if "age_from" in dict_of_targets_params.keys() and "age_to" in dict_of_targets_params.keys():
            res_str += f";\nвозраст от {dict_of_targets_params['age_from']} до {dict_of_targets_params['age_to']}"
        if "city" in dict_of_targets_params.keys():
            res_str += f"\nгород: {dict_of_targets_params['city']}"
        res_str += "."
        return res_str

    def wait_for_user(self):
        vk = self.vk_session.get_api()
        longpoll = VkLongPoll(self.vk_session)
        print('Бот ждёт пользователя.')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
                self.user_data_list.append(get_user_data(self.token, event.user_id))
                self.hello_message(self.user_data_list[0])
                self.user_data_list[0].update({"params_for_search": self.get_params_for_search(self.user_data_list[0])})
                self.write_msg(user_id=self.user_data_list[0].get("id"),
                          message=self.make_target_params_str(self.user_data_list[0].get("params_for_search")))

                self.write_msg(user_id=self.user_data_list[0].get("id"), message=f'Проводим поиск по ВК')
                raw_userslist = search_users_in_vk(token=os.getenv('my_token'),
                                   users_params_to_search=self.user_data_list[0].get("params_for_search"))
                DataBaseСlerk(os.getenv('PG_pasw'), raw_userslist)
