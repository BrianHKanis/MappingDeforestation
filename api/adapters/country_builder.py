import json
from ..models.country import Country

class CountryBuilder:
    tables_dicts = {
        8: {'demographics': 0, 'land_use': 1, 'tropical_primary_loss': 2,
            'tree_loss': 3, 'states': 4},
        5: {'demographics': 0, 'land_use': 1, 'tree_loss': 2, 'states': 3}
        }

    def __init__(self, client_obj):
        self.name = client_obj.country_name
        self.df = client_obj.df
        self.geojson = client_obj.geojson
        self.table_amount = len(client_obj.df)
        self.table_dict = self.tables_dicts[self.table_amount]

    def select_table(self, table_name):
        if not table_name in self.table_dict.keys():
            print(f'{table_name} not found')
            return []
        else:
            index = self.table_dict[table_name]
            selected_table = self.df[index]
            return selected_table
    
    def demographic_table_to_dict(self):
        demographics_table = self.select_table('demographics')
        demographics_dict = dict(zip(demographics_table[0].to_dict().values(), demographics_table[1].to_dict().values()))
        return demographics_dict
    
    def land_use_table_to_dict(self):
        land_use_table = self.select_table('land_use')
        surface_area = int(land_use_table.to_dict()[0][0].split(':')[1].replace(' ', '').replace(',', '')) * 100  #In Hectares 
        tree_cover_totals_list = land_use_table.to_dict()[0][1][17:].replace(' Tree', '--Tree').split('--')
        tree_cover_totals_dict = {}
        for string in tree_cover_totals_list:
            k = string.split(': ')[0]
            v = string.split(': ')[1]
            if len(v) > 6:
                v = int(v.replace(',', ''))
            tree_cover_totals_dict[k] = v
        land_use_dict = {'surface_area' : surface_area, 'totals': tree_cover_totals_dict}
        return land_use_dict
    
    def tree_loss_table_to_dict(self):
        tree_loss_table = self.select_table('tree_loss')
        tree_loss_list = tree_loss_table.to_dict()[0][0][15:].split(':')
        tree_loss_years = []
        tree_loss_areas = []
        for i in range(0, len(tree_loss_list)-1):
            tree_loss_year = tree_loss_list[i][-4:]
            tree_loss_years.append(int(tree_loss_year))
            forest_area = tree_loss_list[i+1].split(' ')[1]
            tree_loss_areas.append(int(forest_area.replace(',', '')))
        tree_loss_dict = dict(zip(tree_loss_years, tree_loss_areas))
        return tree_loss_dict

    def all_tables_to_dict(self): 
        cleaned_tables = {'demographics': self.demographic_table_to_dict(), 'land_use': self.land_use_table_to_dict(), 'tree_loss': self.tree_loss_table_to_dict()}
        return cleaned_tables

    def select_attributes(self):
        tables = self.all_tables_to_dict()
        country_dict = {}
        country_dict['name'] = self.name
        country_dict['geojson'] = self.geojson
        country_dict['area'] = tables['land_use']['surface_area']
        return country_dict
    
    def run(self, country_dict):
        country_dict = self.select_attributes()
        country_obj = Country(**country_dict)
        return country_obj

    

    
