import pandas as pd
from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities



#---------COMMANDS---------#

doors = acc.GetElementsByType('Door')
zones = acc.GetElementsByType('Zone')

propertyUserIds = acu.GetBuiltInPropertyId('General_ElementID')


def x():
    for i in range(len(acc.GetPropertyValuesOfElements(doors, [propertyUserIds]))):
        for i2 in range(len(acc.GetPropertyValuesOfElements(doors, [propertyUserIds])[i].propertyValues)):
            x = acc.GetPropertyValuesOfElements(doors, [propertyUserIds])[i].propertyValues[i2].propertyValue.value
            print(x)

#print(acc.GetElementsRelatedToZones(zones, doors))

#print(acc.GetPropertyValuesOfElements(doors, [propertyUserIds])[0].propertyValues)
print('hello world')

