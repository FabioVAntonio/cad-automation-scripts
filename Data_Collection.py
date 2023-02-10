import pandas as pd
import numpy as np
import csv
import time
import sys
import os

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

#---------COMMANDS---------#
#print(acc.GetAllPropertyNames())   #gets all builtin and userdefinded property names

doors = acc.GetElementsByType('Door')
zones = acc.GetElementsByType('Zone')


general_element_ID = acu.GetBuiltInPropertyId('General_ElementID')
room_number = acu.GetUserDefinedPropertyId('Türen + Tore + Fenster', 'Raumnummer')
room_name = acu.GetUserDefinedPropertyId('Türen + Tore + Fenster', 'Raumname')

#---------COMMANDS---------#


#---------good to know-------#
#list(dict.fromkeys(array_complete_room_names)) #---> deletes duplicates in the array


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
    def __init__(self, element, ID):
        self.element = element
        self.ID = ID

    def values(self):
        array_values = []       #always in index order 1, 2, 3, 4, 5, ...
                                                                                                                                                                                                    #length of 3d array of elementIds: [[ElementIdArrayItem {'elementId': {'guid': '4812C19F-B046-480E-96BB-2B96EF831FBA'}}, ...]]
        array_values = [acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{acc.GetElementsByType(self.element)[i].elementId.guid}'}}], [self.ID])[0].propertyValues[0].propertyValue.value for i in range(len(acc.GetElementsByType(self.element)))]  #outputs each value after gettng guid and parsing it in
        return array_values


class y:
    def __init__(self, file, element, ID):
        self.file = file
        self.element = element
        self.ID = ID

    def newvalues(self):    #visual
        df = pd.read_csv(f'{self.file}')
        newdata = [{x(self.element, self.ID).values()[i] : 'new'} if x(self.element, self.ID).values()[i] not in df.values else {x(self.element, self.ID).values()[i] : 'current'} for i in range(len(x(self.element, self.ID).values()))]
        return newdata

    def newindexes(self):
        df = pd.read_csv(f'{self.file}')
        newdata_indexes = [i if x(self.element, self.ID).values()[i] not in df.values else None for i in range(len(x(self.element, self.ID).values()))]
        return newdata_indexes

        


#print(y('C:\\Users\\fabio\\OneDrive\\Dokumente\\Coding\\IFCnAPI_Project\\IFCnAPI_Code\\Output\\test_v1.csv', 'Door', general_element_ID).newvalues())  #outputs: [{'WE 003 T1': 'current'}, {'WE 002 T1': 'current'}, {'WE 002 T2': 'current'}, {'WE 000 T1': 'current'}, {'WE 001 T1': 'current'}, {'WE 002 T3': 'current'}, {'WE 004 T1': 'current'}, {'WE 002 T4': 'current'}, {'WE 000 T2': 'current'}]

#print(x('Door', general_elmenent_ID).values())     #outputs: ['T000', 'T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008']
#print(x('Door', room_number).values())  #outputs: ['', 'WE 003', 'WE 002', 'WE 002', '', 'WE 001', 'WE 002', 'WE 004', 'WE 002']
#print(x('Door', room_name).values())  #outputs: ['Wohnen', 'Wohnen', 'Wohnen', 'Wohnen', 'Wohnen', 'Wohnen', 'WC', 'Küche', 'WC']






#studying how archicad reads elements related to zone (in this case doors)
array_relation = []
array_elements = []
array_room_number = []
array_merged_keys = {}
array_merged_keys_index = {}
array_complete_room_names = []

def getdata(element):
    n = 0
    for i in range(len(acc.GetElementsRelatedToZones(zones, [element]))):    #3d array of elementIds:    [[ElementIdArrayItem {'elementId': {'guid': '4812C19F-B046-480E-96BB-2B96EF831FBA'}}, ...]]
        for i2 in range(len(acc.GetElementsRelatedToZones(zones, [element])[i].elements)):   #gets length of each nested array
            guid = (acc.GetElementsRelatedToZones(zones, [element])[i].elements[i2].elementId.guid)  #gets each guid in each nested array
            array_relation.append({x('Zone', general_element_ID).values()[n]: acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{guid}'}}], [general_element_ID])[0].propertyValues[0].propertyValue.value}) #converts guid to readable property name, for e.g.: 'T005'
            array_elements.append(acc.GetPropertyValuesOfElements([{'elementId': {'guid': f'{guid}'}}], [general_element_ID])[0].propertyValues[0].propertyValue.value)
            array_room_number.append(x('Zone', general_element_ID).values()[n])
        n += 1

#output of print(elements_in_zone()) in relation test data: ---> [{'WE 000': 'T003'}, {'WE 000': 'T004'}, {'WE 000': 'T000'}, {'WE 001': 'T005'}, {'WE 001': 'T004'}, {'WE 002': 'T002'}, {'WE 002': 'T003'}, {'WE 003': 'T001'}, {'WE 001': 'T007'}, {'WE 002': 'T006'}, {'WE 002': 'T008'}, {'WE 004': 'T008'}, {'WE 004': 'T007'}]
#output of print(elements_in_zone()) in elements test data: ---> ['T003', 'T004', 'T000', 'T005', 'T004', 'T002', 'T003', 'T001', 'T007', 'T006', 'T008', 'T008', 'T007']
#output of print(elements_in_zone()) in elements test data: ---> ['WE 000', 'WE 000', 'WE 000', 'WE 001', 'WE 001', 'WE 002', 'WE 002', 'WE 003', 'WE 001', 'WE 002', 'WE 002', 'WE 004', 'WE 004']

                                                                                        #for e.g. for index i = 0 (T000) outputs ---> [2]     #if room has no room number                   #just gets available room number   #everything happens in range of total amount of room number
    array_complete_room_names = [(array_room_number[(all_indexes_of_items(array_elements, x(element, general_element_ID).values()[i]))[0]]) if x(element, room_number).values()[i] == '' else x(element, room_number).values()[i] for i in range(len(x(element, room_number).values()))]
    #return array_complete_room_names   #---> outputs: ['WE 000', 'WE 003', 'WE 002', 'WE 002', 'WE 000', 'WE 001', 'WE 002', 'WE 004', 'WE 002']

#----------------------

                                        #ArchiCAD reads everything related to zone order (acc.GetElementsRelatedToZones() works in coherant order of rooms)
            #print(array_elements)       output:               ['T003', 'T004', 'T000',   'T005', 'T004',   'T002', 'T003',    'T001',     'T007',    'T006', 'T008',   'T008', 'T007']
            #print(x('Zone', general_elmenent_ID).values())    [       'WE 000',             'WE 001',        'WE 002',       'WE 003',   'WE 001',     'WE 002',          'WE 004']

#next step would be attributing each door to the correct room

    #puts data into order: [{'WE NNN': 'TXXX'}, {'WE NNN': 'TXXX'},
    dataset = [{array_complete_room_names[i] : x('Door', general_element_ID).values()[i]} for i in range(len(array_complete_room_names))]
    dataset_indexes = [{array_complete_room_names[i] : i} for i in range(len(array_complete_room_names))]
    dataset_indicator = [{array_complete_room_names[i] : list(y('C:\\Users\\fabio\\OneDrive\\Dokumente\\Coding\\IFCnAPI_Project\\IFCnAPI_Code\\Output\\test_v1.csv', 'Door', general_element_ID).newvalues()[i].values())[0]} for i in range(len(array_complete_room_names))]
    #return dataset     #--> output: [{'WE 000': 'T000'}, {'WE 003': 'T001'}, {'WE 002': 'T002'}, {'WE 002': 'T003'}, {'WE 000': 'T004'}, {'WE 001': 'T005'}, {'WE 002': 'T006'}, {'WE 004': 'T007'}, {'WE 002': 'T008'}]
    #return dataset_indexes      #--> output: [{'WE 000': 0}, {'WE 003': 1}, {'WE 002': 2}, {'WE 002': 3}, {'WE 000': 4}, {'WE 001': 5}, {'WE 002': 6}, {'WE 004': 7}, {'WE 002': 8}]

#---------------------
    #merging same keys together
    for dict1, dict2 in zip(dataset, dataset_indexes):
        for key1, key2 in zip(dict1, dict2):
            try:
                array_merged_keys[key1].append(dict1[key1])
                array_merged_keys_index[key2].append(dict2[key2])
            except KeyError:
                array_merged_keys[key1] = [dict1[key1]]
                array_merged_keys_index[key2] = [dict2[key2]]
    return array_merged_keys   #output: {'WE 003': ['T000'], 'WE 002': ['T001', 'T002', 'T005', 'T007'], 'WE 000': ['T003', 'T008'], 'WE 001': ['T004'], 'WE 004': ['T006']}
    #return array_merged_keys_index      #output: {'WE 000': [0, 4], 'WE 003': [1], 'WE 002': [2, 3, 6, 8], 'WE 001': [5], 'WE 004': [7]}


def savedata():
    #write data to csv file
    print('Saving data...')
    csv_data = []
    for i in range(len(array_merged_keys)):
        for i2 in range(len(list(array_merged_keys.values())[i])):
            csv_data.append(({'Raumnummer': list(array_merged_keys.keys())[i], 'Raumname': x('Door', room_name).values()[i], 'Element-ID': list(array_merged_keys.values())[i][i2], 'Element_Index': f'{list(array_merged_keys_index.values())[i][i2]}'}))

    df = pd.DataFrame(csv_data, columns = ['Raumnummer', 'Raumname', 'Element-ID', 'Element_Index'])
    #work on grouping Zones (insert finished code here)
    #insert here
    filename = input('Save to which file? Enter here: ')
    df.to_csv(f'C:\\Users\\fabio\\OneDrive\\Dokumente\\Coding\\IFCnAPI_Project\\IFCnAPI_Code\\Output\\{filename}.csv', mode='w')
    print(df)
    return 'Data has been saved. See the preview above'


def rename(element):
    getdata(element)
    print('Starting renaming Process...')
    for i in range(len(array_merged_keys)):
        n = 0
        for i2 in (list(array_merged_keys_index.values())[i]):
            n += 1      
            acc.SetPropertyValuesOfElements([act.ElementPropertyValue(acc.GetElementsByType('Door')[i2].elementId, general_element_ID, act.NormalStringPropertyValue(f'{list(array_merged_keys.keys())[i]} T{n}'))])
    return 'Process done.'



#print(rename('Door'))
#print(getdata('Door'))
#print(savedata())


#work list:
#addition of Doors: CORRECT(works)
#!!!subtraction of Doors: work on order of doors if one door gets deleted
#!!!if door opens out of room into 'nothing' (renaming works, appending data to csv doesnt)



#test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#df = pd.read_csv('C:\\Users\\fabio\\OneDrive\\Dokumente\\Coding\\IFCnAPI_Project\\IFCnAPI_Code\\Output\\test_v1.csv')
#print((df['Raumnummer']=='WE 000').sum())   #'not iterable': google for numpy iteration








#print(acc.GetElementsRelatedToZones([zones][0], zones))
print(acc.GetPropertyValuesOfElements([{'elementId': {'guid': '158ED699-99F8-4376-AE93-2EFC1AB556B7'}}], [general_element_ID])[0].propertyValues[0].propertyValue.value)


#-----stops time-----#
end = time.time()
print('Runtime is:', (end-start) * 1, 's')