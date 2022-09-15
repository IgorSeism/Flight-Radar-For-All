import pandas as pd
import collections

def count_cities_origin_xlxs(path):  # /функция считает каунтер для городов вылета
    counter = collections.Counter()
    df = pd.read_excel(path, sheet_name='All flights')
    origin_city = pd.DataFrame(df, columns=['Origin_city'])

    for i in range(0, len(origin_city)):
        counter[origin_city.loc[i][0]] += 1
    return counter


def count_cities_destination_xlxs(path):  # /функция считает каунтер для городов прилета
    counter = collections.Counter()
    df = pd.read_excel(path, sheet_name='All flights')
    destination_city = pd.DataFrame(df, columns=['Destination_city'])

    for i in range(0, len(destination_city)):
        counter[destination_city.loc[i][0]] += 1
    return counter


def count_cities_pairs_xlxs(path):  # /функция считает каунтер для пар городов вылета-прилета
    counter = collections.Counter()
    df = pd.read_excel(path, sheet_name='All flights')
    origin_city = pd.DataFrame(df, columns=['Origin_city'])
    destination_city = pd.DataFrame(df, columns=['Destination_city'])

    for i in range(0, max(len(origin_city), len(destination_city))):
        if type(origin_city.loc[i][0]) is str and type(destination_city.loc[i][0]) is str:
            counter[origin_city.loc[i][0] + ' - ' + destination_city.loc[i][0]] += 1
    return counter
# -----------------------------------------
def count_coutries_origin_xlxs(path):  # /функция считает каунтер для городов вылета
    counter = collections.Counter()
    df = pd.read_excel(path, sheet_name='All flights')
    origin_country = pd.DataFrame(df, columns=['Origin_country'])

    for i in range(0, len(origin_country)):
        counter[origin_country.loc[i][0]] += 1
    return counter


def count_coutries_destination_xlxs(path):  # /функция считает каунтер для городов прилета
    counter = collections.Counter()
    df = pd.read_excel(path, sheet_name='All flights')
    destination_country = pd.DataFrame(df, columns=['Destination_country'])

    for i in range(0, len(destination_country)):
        counter[destination_country.loc[i][0]] += 1
    return counter


def count_coutries_pairs_xlxs(path):  # /функция считает каунтер для пар городов вылета-прилета
    counter = collections.Counter()
    df = pd.read_excel(path, sheet_name='All flights')
    origin_country = pd.DataFrame(df, columns=['Origin_country'])
    destination_country = pd.DataFrame(df, columns=['Destination_country'])

    for i in range(0, max(len(origin_country), len(destination_country))):
        if type(origin_country.loc[i][0]) is str and type(destination_country.loc[i][0]) is str:
            counter[origin_country.loc[i][0] + ' - ' + destination_country.loc[i][0]] += 1
    return counter

path = r"result_G600.xlsx" # /путь файла со всеми полетами

# чтение файла со всеми полетами и подсчет нужных каунтеров
counter_cities_origin = count_cities_origin_xlxs(path)
counter_cities_destination = count_cities_destination_xlxs(path)
counter_cities_pairs = count_cities_pairs_xlxs(path)

counter_coutries_origin = count_coutries_origin_xlxs(path)
counter_coutries_destination = count_coutries_destination_xlxs(path)
counter_coutries_pairs = count_coutries_pairs_xlxs(path)


# объединение пар с одинаковыми именами (Москва - Казань, Казань - Москва)
counter_1 = collections.Counter()
for a,b in counter_cities_pairs.items():
    s: list = a.split(' - ')
    s.sort()
    new_key = ' - '.join(s)
    counter_1[new_key] += b

counter_2 = collections.Counter()
for a,b in counter_coutries_pairs.items():
    s: list = a.split(' - ')
    s.sort()
    new_key = ' - '.join(s)
    counter_2[new_key] += b

counter_cities_origin_xlxs = pd.DataFrame(counter_cities_origin.items(), columns=["cities_origin", "Value"])
counter_cities_destination_xlxs = pd.DataFrame(counter_cities_destination.items(), columns=["cities_destination", "Value"])
counter_cities_pairs_xlxs = pd.DataFrame(counter_1.items(), columns=["Pair", "Value"])

counter_coutries_origin_xlxs = pd.DataFrame(counter_coutries_origin.items(), columns=["coutries_origin", "Value"])
counter_coutries_destination_xlxs = pd.DataFrame(counter_coutries_destination.items(), columns=["coutries_destination", "Value"])
counter_coutries_pairs_xlxs = pd.DataFrame(counter_2.items(), columns=["Pair", "Value"])

# запись в сохраняемый файл
with pd.ExcelWriter(path, engine="openpyxl", mode= 'a') as writer: 
    counter_cities_origin_xlxs.to_excel(writer, sheet_name='Origin_cities')
    counter_cities_destination_xlxs.to_excel(writer, sheet_name='Destination_cities')
    counter_cities_pairs_xlxs.to_excel(writer, sheet_name='Pairs_cities')

    counter_coutries_origin_xlxs.to_excel(writer, sheet_name='Origin_coutries')
    counter_coutries_destination_xlxs.to_excel(writer, sheet_name='Destination_coutries')
    counter_coutries_pairs_xlxs.to_excel(writer, sheet_name='Pairs_coutries')
