# testing IFCOpenshell
from fileinput import filename
import ifcopenshell
from ifcopenshell.util.selector import Selector


ifc = ifcopenshell.open('./IFCs and PLNs/Test.ifc')
ifc_objects = ifcopenshell.open('./IFCs and PLNs/Objects.ifc')
selector = Selector()



wall = ifc.by_type('IfcWall')[0]
zones = ifc.by_type('IfcSpace')
zone = ifc.by_type('IfcSpace')[0]
door = ifc.by_type('IfcDoor')[0]

object = ifc_objects.by_type('IfcFurniture')
test_objects = ifc.by_type('IfcFurniture')

#print(wall.get_info())      #gets: id , type, GlobalId, OwnerHistory, Name, etc.. in key/value pairs
#print(wall.get_info().get('Name'))  #pick out specific info  or in short: print(wall.Name)


test_objects[-2] = object   #changing of objects

print(test_objects[-2])


ifc = ifc.write('./IFCs and PLNs/Test.ifc')    #overwrites current IFC file


#elements = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')
#elements_2 = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')[4]
#print(elements_2)

