#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import time
import datetime
import rsa_decoder
import sqlite3

connection = sqlite3.connect('shows.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Shows
              (data_now  DATETIME,
                leakage_sensor_1 FLOAT,
                smoke_sensor_1 FLOAT,
                gas_leak_sensor FLOAT,
                temp_sensor FLOAT,
                humidity_sensor FLOAT,
                motion_sensor_1 FLOAT,
                opening_sensor_1 FLOAT)''')
cursor.execute("DELETE FROM Shows")

data_now = []

def rescale(value, old_min, old_max, new_min, new_max):
    rescaled = (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
    return rescaled

rsa_decoder.generate_keys()

# (key_pub, key_priv) = rsa.newkeys(512)

while 1:
    time.sleep(5)
    # датчик контроля протечек
    leakage_sensor = np.random.binomial(10, 0.5)
    leakage_sensor = rescale(leakage_sensor, 0, 10, 0, 1)
    leakage_sensor_1 = round(leakage_sensor)
    # датчик задымления !!!
    smoke_sensor = np.random.gumbel(0, 1)
    smoke_sensor = rescale(smoke_sensor, -5, 6, 0, 1)
    smoke_sensor_1 = round(smoke_sensor)
    # датчик утечки газа
    gas_leak_sensor = np.random.laplace(loc=0.0, scale=1.0, size=None)
    gas_leak_sensor = rescale(gas_leak_sensor, -5, 5, 0, 50)
    # датчик температуры
    temp_sensor = np.random.power(0.7)
    temp_sensor = rescale(temp_sensor, 0, 1, 0, 50)
    # датчик влажности воздуха
    humidity_sensor = np.random.uniform(0, 100)
    # датчик движения
    motion_sensor = np.random.weibull(2)
    motion_sensor = rescale(motion_sensor, 0, 3, 0, 1)
    motion_sensor_1 = round(motion_sensor)
    # датчик открытия окон и дверей
    opening_sensor = np.random.normal(100, 10)
    opening_sensor = rescale(opening_sensor, 70, 120, 0, 1)
    opening_sensor_1 = round(opening_sensor)

    data_now = datetime.datetime.now()
#     moreShows = [(data_now,
#                 rsa.encrypt((str(leakage_sensor_1)).encode('utf8'), key_pub),
#                 rsa.encrypt((str(smoke_sensor_1)).encode('utf8'), key_pub),
#                 rsa.encrypt((str(gas_leak_sensor)).encode('utf8'), key_pub),
#                 rsa.encrypt((str(temp_sensor)).encode('utf8'), key_pub),
#                 rsa.encrypt((str(humidity_sensor)).encode('utf8'), key_pub),
#                 rsa.encrypt((str(motion_sensor_1)).encode('utf8'), key_pub),
#                 rsa.encrypt((str(opening_sensor_1)).encode('utf8'), key_pub))]
#     moreShows = [(data_now,
#                 leakage_sensor_1,
#                 smoke_sensor_1,
#                 gas_leak_sensor,
#                 temp_sensor,
#                 humidity_sensor,
#                 motion_sensor_1,
#                 opening_sensor_1)]
    moreShows = [(rsa_decoder.encode(data_now),
                rsa_decoder.encode(leakage_sensor_1),
                rsa_decoder.encode(smoke_sensor_1),
                rsa_decoder.encode(gas_leak_sensor),
                rsa_decoder.encode(temp_sensor),
                rsa_decoder.encode(humidity_sensor),
                rsa_decoder.encode(motion_sensor_1),
                rsa_decoder.encode(opening_sensor_1))]


    cursor.executemany("INSERT INTO Shows VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)", moreShows)
    connection.commit()

    cursor.execute("SELECT * FROM Shows")
    results = cursor.fetchall()
    print(results)
    
#     
#     cursor.close()


# In[ ]:




