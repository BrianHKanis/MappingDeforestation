import requests
import pandas as pd
import json

column_names = ['Sub-national admin area 1 Tree cover extent (2001) ha',
'Tree cover loss (2001-05) ha', 'Tree cover loss (2001-05) ha',
'Tree cover loss (2006-10) ha', 'Tree cover loss (2011-15) ha',
'Tree cover loss (2016-20) ha', 'Tree cover loss (2001-20) ha',
'Tree cover loss (2001-20) %']



class Client:
    URL = 'https://rainforests.mongabay.com/deforestation/archive/'
    geourl = 'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/'
    ecu_url = 'https://raw.githubusercontent.com/pabl-o-ce/Ecuador-geoJSON/master/geojson/ecuador.geojson'
    # areas = 'https://en.wikipedia.org/wiki/List_of_North_American_countries_by_area'

    def __init__(self, country_name):
        self.country_name = country_name.capitalize()
        self.df = self.get_dataframe()
        self.geojson = self.get_geojson()
        # self.area = self.get_area()

    def get_dataframe(self):
        url = self.URL + self.country_name + '.htm'
        response = requests.get(url)
        df = pd.read_html(response.content)
        return df

    def get_geojson(self):
        url = self.geourl + self.country_name.lower().replace('_', '-') + '.geojson'
        response = requests.get(url)
        if self.country_name == 'Ecuador':
            response = requests.get(self.ecu_url)
        if response.status_code != 200:
            print('Geojson url not found')
            print('Please paste the geojson path here or pick another country')
            path = input()
            if 'http' in path:
                response = requests.get(path)
                breakpoint()
            else:
                with open(path, 'r') as f:
                    return json.load(f)
        return json.loads(response.content)

    # def get_area(self):
    #     url = self.areas
    #     df = pd.read_html(url)
    #     country_name = self.country_name.replace('_', ' ')
    #     countries_list = df[0].to_dict('records')
    #     selected = [country for country in countries_list if country['Country / territory'] == country_name]
    #     area = selected[0]['North America area in km2 (mi2)']
    #     hectares = int(area.split(' ')[0].replace(',', '').replace("'", '')) * 100
    #     return hectares
    