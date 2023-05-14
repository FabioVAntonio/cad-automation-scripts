# testing IFCOpenshell
from fileinput import filename
import ifcopenshell
from ifcopenshell.util.selector import Selector


ifc = ifcopenshell.open('./IFCs and PLNs/Test.ifc')
selector = Selector()



wall = ifc.by_type('IfcWall')[0]
zones = ifc.by_type('IfcSpace')
zone = ifc.by_type('IfcSpace')[0]
door = ifc.by_type('IfcDoor')[0]

#print(wall.get_info())      #gets: id , type, GlobalId, OwnerHistory, Name, etc.. in key/value pairs
#print(wall.get_info().get('Name'))  #pick out specific info  or in short: print(wall.Name)

zones[2].Name = 'Test room number'
#print(door.get_info().get('Name'))
print(zones[2].Name)
ifc = ifc.write('./IFCs and PLNs/Test.ifc')


#elements = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')
#elements_2 = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')[4]
#print(elements_2)

