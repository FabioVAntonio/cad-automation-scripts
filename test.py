import renaming as r
import pandas as pd

from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities


walls = acc.GetElementsByType('Wall')

ElementID = acu.GetBuiltInPropertyId('General_ElementID')
wall_info = acu.GetUserDefinedPropertyId('API', 'mehrschichtige Bauteile')
wall_info2 = acu.GetUserDefinedPropertyId('API', 'Baustoff')
Raumnummer = acu.GetUserDefinedPropertyId('Türen + Tore + Fenster', 'Raumnummer')
Raumname = acu.GetUserDefinedPropertyId('Türen + Tore + Fenster', 'Raumname')

print(r.x('Wall', ElementID, 'C:\\Users\\fabio\\OneDrive\\Dokumente\\Coding\\main_project\\main_code\\Output\\wall_materials.csv').values()[0])

for i in range(len(acc.GetElementsByType('Wall'))):
    acc.SetPropertyValuesOfElements([act.ElementPropertyValue(acc.GetElementsByType('Wall')[i].elementId, ElementID, act.NormalStringPropertyValue(f'Test{i}'))])

print(r.x('Wall', ElementID, 'C:\\Users\\fabio\\OneDrive\\Dokumente\\Coding\\main_project\\main_code\\Output\\wall_materials.csv').values())