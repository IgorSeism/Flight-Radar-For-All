import pandas as pd
import collections
import re

from flight_radar import Client

def get_reg_num_list(path):
    df = pd.read_excel(path)
    column_reg = pd.DataFrame(df, columns=['Registration'])
    list_of_reg = []

    for i in range(0, len(column_reg.index)):
        if type(column_reg.loc[i][0]) is str and len(column_reg.loc[i][0])>=4 and not (re.findall(r'[+/]',column_reg.loc[i][0])):
            list_of_reg.append(column_reg.loc[i][0])

    return list_of_reg


counter_country = collections.Counter()
counter_city = collections.Counter()
c = Client(
        '***@yandex.ru',
        '***'
    )

c.login()

qq = get_reg_num_list(r'G600.xlsx')
result = []

for q in qq:
    print(q)
    for fd in c.iter_flights(q):
        if counter_country[fd.countries[0]] == counter_country[fd.countries[1]]:
            counter_country[fd.countries[0]] += 1
        else:
            counter_country.update(fd.countries)

        if counter_city[fd.origin_city] == counter_city[fd.destination_city]:
            counter_city[fd.origin_city] += 1
        else:
            counter_city[fd.origin_city] += 1
            counter_city[fd.destination_city] += 1
        result.append([fd.origin_city, fd.destination_city,
                       fd.countries[0], fd.countries[1],
                       fd.departure_datetime, fd.arrival_datetime,
                       fd.coordinates_city_origin, fd.coordinates_city_destination])
        print(fd)


c.logout()
result_xlsx = pd.DataFrame(result, columns=['Origin_city', 'Destination_city',
                                            'Origin_country', 'Destination_country',
                                            'Date_departure', 'Date_arrival',
                                            'Coordinates_city_origin', 'Coordinates_city_destination'])

counter_country_xlsx = pd.DataFrame(counter_country.items(), columns=["Country", "Value"])
counter_city_xlsx = pd.DataFrame(counter_city.items(), columns=["City", "Value"])
with pd.ExcelWriter("result_Global.xlsx") as writer:
    result_xlsx.to_excel(writer, sheet_name='All flights')
    counter_country_xlsx.to_excel(writer, sheet_name='Counter_countries')
    counter_city_xlsx.to_excel(writer, sheet_name='Counter_city')
