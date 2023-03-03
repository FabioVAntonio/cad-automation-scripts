# testing IFCOpenshell
from fileinput import filename
import ifcopenshell
from ifcopenshell.util.selector import Selector


ifc = ifcopenshell.open('C:/Users/fabio/OneDrive/Dokumente/Coding/IFCnAPI_Project//IFCnAPI_Code/IFCs and PLNs/Test.ifc')
selector = Selector()



wall = ifc.by_type('IfcWall')[0]
zones = ifc.by_type('IfcSpace')
zone = ifc.by_type('IfcSpace')[0]
door = ifc.by_type('IfcDoor')[0]

#print(wall.get_info())      #gets: id , type, GlobalId, OwnerHistory, Name, etc.. in key/value pairs
#print(wall.get_info().get('Name'))  #pick out specific info

#print(zone.get_info().get('Name'))  #or in short: print(zone.Name)
print(door.get_info().get('Name'))
print(zones[2].Name)


elements = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')[2]
elements_2 = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')[4]
print(elements)

