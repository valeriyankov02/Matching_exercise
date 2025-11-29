import re
import pandas as pd

dataset1 = pd.read_csv('Dataset1.csv')
dataset2 = pd.read_csv('Dataset2.csv')

def normalize_dataset1():
    for x in range(len(dataset1['supplier_catalog_id'])):
        cell = re.search(r"ab(\d{4,6})",dataset1.loc[x, 'supplier_catalog_id'])
        if(cell != None):
            dataset1.loc[x, 'supplier_catalog_id'] = cell.group()

def normalize_dataset2():
    for x in range(len(dataset2['supplier_catalog_id'])):
        cell = re.search(r"ab(\d{4,6})",dataset2.loc[x, 'supplier_catalog_id'])
        if(cell != None):
            dataset2.loc[x, 'supplier_catalog_id'] = cell.group()

def fill_samples_size_dataset2():
    for x in range(len(dataset2['samples_size'])):
        if not (isinstance(dataset2.loc[x, 'samples_size'], str)):
            cell = re.search(r"[0-9]+[^0-9]+?(?=\s)",dataset2.loc[x, 'product name'])
            if (cell != None):
                dataset2.loc[x, 'samples_size'] = cell.group()

def fix_samples_size_dataset2():
    for x in range(len(dataset2['samples_size'])):
        if (isinstance(dataset2.loc[x, 'samples_size'], str)):
            dataset2.loc[x, 'samples_size'] = dataset2.loc[x, 'samples_size'].replace('ul', 'µl')
            dataset2.loc[x, 'samples_size'] = dataset2.loc[x, 'samples_size'].replace('ug', 'µg')
            cell = re.search(r"^(\d+)(\D+)(?=\s|$)", dataset2.loc[x, 'samples_size'])
            dataset2.loc[x, 'samples_size'] = cell.group(1) + ' ' + cell.group(2)

def fix_dataset3():
    dataset3['samples_size'] = dataset3['samples_size_x'].combine_first(dataset3['samples_size_y'])
    dataset3.drop(['samples_size_x', 'samples_size_y'], axis=1, inplace=True)
    for x in range(len(dataset3['supplier_catalog_id'])):
        dataset3.loc[x, 'product name'] = 'example name - ' + dataset3.loc[x, 'supplier_catalog_id'] + ' - ' + dataset3.loc[x, 'samples_size']
    dataset3.drop_duplicates(subset=['supplier_catalog_id'], inplace=True)
    dataset3.reset_index(drop=True, inplace=True)

normalize_dataset1()
normalize_dataset2()

fill_samples_size_dataset2()
fix_samples_size_dataset2()

dataset3 = pd.merge(dataset1, dataset2, on='supplier_catalog_id', how='outer')
fix_dataset3()

print(dataset3.to_string())