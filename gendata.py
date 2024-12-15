from random import random
import psycopg2
from dotenv import dotenv_values

config = dotenv_values()

# Описание элементов ноутбуков
properties = {
	'manufacturers': ['LG', 'HP', 'Lenovo', 'Samsung', 'Asus', 'Acer', 'Apple'],
	'cpus': ['x64', 'ARM', 'RISC-V'],
	'harddrive_types': ['SSD', 'HDD', 'SSD+HDD'],
	'harddrive_spaces': ['<= 128 GB', '128-256GB', '256-512GB', '512-1024GB', '1024+GB'],
	'ram_types': ['DDR3', 'DDR4'],
	'rams': ['1-2GB', '2-4GB', '4-8GB', '8-16GB', '16+GB'],
	'wifis': ['No Wifi', 'Wifi 2.4', 'Wifi 5.8'],
	'bluetooths': ['No Bluetooth', 'Has Bluetooth'],
	'ethernets': ['No Ethernet', 'Has Ethernet'],
	'webcams': ['No Webcam', 'Has Webcam'],
	'cardreaders': ['No Cardreader', 'Has Cardreader'],
	'graphics': ['Integrated GPU', 'External GPU', 'Integrated+External GPU'],
	'displays': ['13.3 inch', '15.6 inch', '16 inch'],
	'usbs': ['No USB', 'USB 2.0', 'USB 3.0'],
	'batteries': ['<= 4 Hours', '4-6 hours', '6-8 hours', '8-10 hours', '10+ hours'],
}
# Определение длины вектора   embedding
vector_len = 0
for p in properties.keys():
	vector_len += len(properties[p])

conn = psycopg2.connect(dbname=config['POSTGRES_DB'], user=config['POSTGRES_USER'], password=config['POSTGRES_PASSWORD'], host="localhost", port=5432)

# Вывод оператора CREATE TABLE, где будут храниться конфигурации ноутбуков
create_table_req =f"""
	CREATE TABLE IF NOT EXISTS laptops(
		id SERIAL PRIMARY KEY,
		manufacturer TEXT NOT NULL,
		cpu TEXT NOT NULL,
		harddrive_type TEXT NOT NULL,
		harddrive_space TEXT NOT NULL,
		ram_type TEXT NOT NULL,
		ram TEXT NOT NULL,
		wifi TEXT NOT NULL,
		bluetooth TEXT NOT NULL,
		ethernet TEXT NOT NULL,
		webcam TEXT NOT NULL,
		cardreader TEXT NOT NULL,
		graphics TEXT NOT NULL,
		display TEXT NOT NULL,
		usb TEXT NOT NULL,
		battery TEXT NOT NULL,
		embedding VECTOR({str(vector_len)}) NOT NULL

);
"""

with conn.cursor() as cursor:
	cursor.execute(create_table_req)
	conn.commit()

inserted = 0 # это текущее число конфигурации ноутбуков
insert_req = ""
for id in range(1, 10_000 + 1): # вместо 1_000_000 надо вставить число конфигураций, которые будут добавлены в БД 
	embedding = []   # это вектор embedding 
	if inserted == 0:
		insert_req += f"INSERT INTO laptops VALUES({str(id)}," # вывести начало оператора INSERT (для первой записи)
	else:
		insert_req += f",({str(id)},"  # вывести начало следующей записи

	for p in properties.keys():  # цикл по свойствам ноутбуков. Начиная с версии Python 3.7, ключи словаря читаются последовательно
		arr = properties[p]  # список вариантов текущего свойства
		i = int(random()*len(arr)) # выбор случайного варианта
		embedding += [ '1' if j == i else '0' for j in range(0, len(arr))] # поместить 1 в позицию вектора для выбранного варианта, остальные 0
		insert_req += f"'{arr[i]}',"
	emb_text = f'[{(','.join(embedding))}]'; # сформировать вектор embedding в виде текста
	insert_req += f"'{emb_text}')" # довавить в описание INSERT вектор embedding

	inserted += 1; # перейти к следующей записи конфигурации
	if inserted >= 1000: 
		with conn.cursor() as cursor:
			cursor.execute(insert_req)
			conn.commit()		
		insert_req = ""
		inserted = 0 # и перейти к новому оператору INSERT

if inserted > 0: 
	with conn.cursor() as cursor:
		cursor.execute(insert_req)
		conn.commit()
