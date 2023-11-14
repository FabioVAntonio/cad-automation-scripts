import pandas as pd
import numpy as np
import csv
import time
import sys
import os
import re

from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

#-----starts time-----#
start = time.time()

def API_status():
    print(acc.IsAlive())

#---------IDS---------#
#print(acc.GetAllPropertyNames())   #gets all builtin and userdefinded property names

doors = acc.GetElementsByType('Door')
zones = acc.GetElementsByType('Zone')


ElementID = acu.GetBuiltInPropertyId('General_ElementID')
Room_number = acu.GetUserDefinedPropertyId('Plugin', 'to room number')
Room = acu.GetUserDefinedPropertyId('Plugin', 'to room')

Width = acu.GetUserDefinedPropertyId('Plugin', 'Width')
Height = acu.GetUserDefinedPropertyId('Plugin', 'Height')


#---------IDS---------#


#---------good to know-------#

#list(dict.fromkeys(array_complete_room_names)) #---> deletes duplicates in the array

#---------good to know-------#



#--------duplicate function---------#

def all_indexes_of_items(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

#--------duplicate function---------#



class x:     #get all values if array contains propertyValues -> propertyValue -> value
    def __init__(self, element, ID, file):
        self.element = element
        self.ID = ID
        self.file = file

    def values(self):
        array_values = []       #always in index order 1, 2, 3, 4, 5, ...
                                                                                                                                                                                                    #length of 3d array of elementIds: [[ElementIdArrayItem {'elementId': {'guid': '4812C19F-B046-480E-96BB-2B96EF831FBA'}}, ...]]
        array_values = [acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [self.ID])[0].propertyValues[0].propertyValue.value for i in range(len(acc.GetElementsByType(self.element)))]  #outputs each value after gettng guid and parsing it in
        return array_values

    def data(self):
        array_relation = []
        for i in range(len(acc.GetElementsByType(self.element))):
            if acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [Room])[0].propertyValues[0].propertyValue.status == 'normal':
                data = {
                        'E1': acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [Room_number])[0].propertyValues[0].propertyValue.value,
                        'E2': acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [Room])[0].propertyValues[0].propertyValue.value,
                        'Element_ID': acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [self.ID])[0].propertyValues[0].propertyValue.value,
                        'Element_Index': i, 
                        }
                array_relation.append(data.values())

        header = ['E1', 'E2', 'Element_ID', 'Element_Index']
        df = pd.DataFrame(array_relation, columns = header)
        df.to_csv(self.file, mode='w')
        return df
    
    def rename(self):
        x(self.element, self.ID, self.file).data()
        df = pd.read_csv(self.file)
        array_merged_keys = {}
        array_merged_keys_index = {}

        dataset = [{acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [Room_number])[0].propertyValues[0].propertyValue.value : acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [self.ID])[0].propertyValues[0].propertyValue.value} for i in range(len(acc.GetElementsByType(self.element)))]
        #[WE X.XX : element id]

        dataset_indexes = [{acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [Room_number])[0].propertyValues[0].propertyValue.value : i} for i in range(len(acc.GetElementsByType(self.element)))]
        #[WE X.XX : element index]

        #merging values of duplicate keys in both data sets
        for dict1, dict2 in zip(dataset, dataset_indexes):
            for key1, key2 in zip(dict1, dict2):
                try:
                    array_merged_keys[key1].append(dict1[key1])
                    array_merged_keys_index[key2].append(dict2[key2])
                except KeyError:
                    array_merged_keys[key1] = [dict1[key1]]
                    array_merged_keys_index[key2] = [dict2[key2]]

        for i in range(len(array_merged_keys)):
            n = 0
            for index in (list(array_merged_keys_index.values())[i]):
                if index in df[df['E2']== 'Kellerabteil' ]['Element_Index'].values:
                    acc.SetPropertyValuesOfElements([act.ElementPropertyValue(acc.GetElementsByType('Door')[index].elementId, ElementID, act.NormalStringPropertyValue(f' Kellerabteil {list(array_merged_keys.keys())[i]} T{1}'))])
                elif 'WE' in list(array_merged_keys.keys())[i]:
                    n += 1      
                    acc.SetPropertyValuesOfElements([act.ElementPropertyValue(acc.GetElementsByType('Door')[index].elementId, ElementID, act.NormalStringPropertyValue(f'{list(array_merged_keys.keys())[i][3:7]} T0{n}'))])
                else:
                    n += 1      
                    acc.SetPropertyValuesOfElements([act.ElementPropertyValue(acc.GetElementsByType('Door')[index].elementId, ElementID, act.NormalStringPropertyValue(f'{list(array_merged_keys.keys())[i]} T0{n}'))])
        
        #appending new data to csv file            
        x(self.element, self.ID, self.file).data()
        return 'Process done.'





#print(df[df['Element_Index']== 0 ]['Element-ID'].values[0])
#print(df[df['Raumname']== 'Kellerabteil' ]['Element_ID'].values)
#print(df['Raumnummer'].values[11])



#print(y('C:\\Users\\fantonio\\Desktop\\ArchiCADAPI\\csv_files\\Türliste_v2.csv', 'Door', ElementID).newvalues())  #outputs: [{'WE 003 T1': 'current'}, {'WE 002 T1': 'current'}, {'WE 002 T2': 'current'}, {'WE 000 T1': 'current'}, {'WE 001 T1': 'current'}, {'WE 002 T3': 'current'}, {'WE 004 T1': 'current'}, {'WE 002 T4': 'current'}, {'WE 000 T2': 'current'}]

#print(x('Door', ElementID).values())     #outputs: ['T000', 'T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008']
#print(x('Door', Raumnummer).values())  #outputs: ['', 'WE 003', 'WE 002', 'WE 002', '', 'WE 001', 'WE 002', 'WE 004', 'WE 002']
#print(x('Door', Raumname).values())  #outputs: ['Wohnen', 'Wohnen', 'Wohnen', 'Wohnen', 'Wohnen', 'Wohnen', 'WC', 'Küche', 'WC']

#print(x('Door', ElementID).data())  #outputs: ['', 'WE 003', 'WE 002', 'WE 002', '', 'WE 001', 'WE 002', 'WE 004', 'WE 002']
#print(x('Door', ElementID).rename())



#-------------------check missing data-----------------#

def check_data(element, Element_IDs, file):
    index_list = []
    missing_elementIDs = []
    df = pd.read_csv(file)
    missing = 0
    correct = 0
    all_elementIDs = x(element, Element_IDs, file).values()
    for ID in all_elementIDs:
        if ID in df['Element_ID'].values:
            boolean = [{'True' : all_elementIDs.index(ID)}]
            index_list.append(boolean)
            correct += 1
        else:
            boolean = [{'False' : all_elementIDs.index(ID)}]
            index_list.append(boolean)
            missing_elementIDs.append(ID)
            missing += 1
    print(f'Number of elements in the project: {len(index_list)}')
    print(f'Number of elements in the dataset: {correct}')
    print(f'Every element has been transferred to the dataset')
    if missing > 0:
        print(f'Number of missing elements: {missing}')
        print(f'Missing elements are: {missing_elementIDs}')

#-------------------check missing data-----------------#


x('Door', ElementID, 'C:\\Users\\fabio\OneDrive\\Dokumente\Coding\\ArchiCADAPI\\main_code\\Output\\Doorlist.csv').rename()
check_data('Door', ElementID, 'C:\\Users\\fabio\OneDrive\\Dokumente\Coding\\ArchiCADAPI\\main_code\\Output\\Doorlist.csv')



#-----stops time-----#
end = time.time()
print('Runtime is:', (end-start) * 1, 's')