from sqlalchemy import create_engine, Table, Column, Integer, MetaData, ForeignKey
from sqlalchemy.types import Boolean, String, Date
from sqlalchemy.sql import select, and_
import time
import datetime


class DataBaseСlerk:
    def __init__(self, dbpassword, list_of_targets):
        self.dbpassword = dbpassword    #o12KinvJdE
        #print ('Начали')
        engine = create_engine(f"postgresql://postgres:{self.dbpassword}@localhost:5432/vk_searchdb", echo=True)
        meta = MetaData(engine)
        conn = engine.connect()
        #
        # oneSearch = Table('oneSearch', meta,  #данные одного поиска
        #     Column('Search_id', Integer, primary_key=True),
        #     Column('user_id', String(250), nullable = False),
        #     Column('user_full_years', String(250), nullable = True),
        #     Column('user_sex', String(250), nullable = True),
        #     Column('user_city', String(250), nullable = True)
        # )
        human = Table('human', meta,    #Найденный поиском человек
                      Column('id', Integer, primary_key=True),
                      Column('vk_id', String(250), nullable=False),
                      # Column('Search_id', String(250), ForeignKey("oneSearch.Search_id")),
                      Column('first_name', String(250), nullable=True),
                      Column('last_name', String(250), nullable=True),
                      Column('can_access_closed', Boolean, nullable=False),
                      Column('is_closed', Boolean, nullable=True),
                      #Column('bdate', Date, nullable=True),
                      Column('bdate', String(50), nullable=True),
                      Column('relation', Integer, nullable=True)
        )
        meta.create_all(engine)
        for target in list_of_targets:
            temp_target = {'id': 0,
            'first_name':'None',
            'last_name':'None',
            'can_access_closed': False,
            'is_closed': False,
            'bdate':  "01.01.2022",
            'relation': 0}

            for key in temp_target:
                if key in target.keys():
                    temp_target.update({key: target[key]})

            # bdate = datetime.datetime.strptime('01.01.2022', "%d.%m.%Y")
            # if 'bdate' in target.keys():
            #     if len(target['bdate'].split('.')) == 3:
            #         bdate = datetime.datetime.strptime(target['bdate'], "%d.%m.%Y")
            #     elif len(target['bdate'].split('.')) == 2:
            #         bdate = datetime.datetime.strptime(target['bdate']+'.2022', "%d.%m.%Y")
            # temp_target.update({'bdate': bdate})

            one_target_add = human.insert().values(vk_id=temp_target['id'],
                                                   first_name=temp_target['first_name'],
                                                   last_name=temp_target['last_name'],
                                                   can_access_closed=temp_target['can_access_closed'],
                                                   is_closed=temp_target['is_closed'],
                                                   bdate=temp_target['bdate'],
                                                   relation=temp_target['relation']
                                                   )
            conn.execute(one_target_add)