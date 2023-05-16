# testing IFCOpenshell
import multiprocessing
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
from ifcopenshell.util.selector import Selector
from ifcopenshell.util.placement import get_local_placement


ifc = ifcopenshell.open('./IFCs and PLNs/Test.ifc')
ifc_objects = ifcopenshell.open('./IFCs and PLNs/Objects.ifc')
selector = Selector()



wall = ifc.by_type('IfcWall')[0]
zones = ifc.by_type('IfcSpace')
zone = ifc.by_type('IfcSpace')[0]
doors = ifc.by_type('IfcDoor')

object = ifc_objects.by_type('IfcFurniture')
test_objects = ifc.by_type('IfcFurniture')

#print(wall.get_info())      #gets: id , type, GlobalId, OwnerHistory, Name, etc.. in key/value pairs
#print(wall.get_info().get('Name'))  #pick out specific info  or in short: print(wall.Name)



#placement_matrix = get_local_placement(test_objects[-2].ObjectPlacement)
#print(placement_matrix)

#test_objects[-2] = object   #changing of objects



#print(test_objects[-2])


#ifc = ifc.write('./IFCs and PLNs/Test.ifc')    #overwrites current IFC file


#elements = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')
#elements_2 = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')[4]



#location of door[0] (as an example) with its nearest IfcSpace
matrix = get_local_placement(doors[0].ObjectPlacement)
location = tuple(map(float, matrix[0:3,3]))
#print(location)


tree_settings = ifcopenshell.geom.settings()
tree_settings.set(tree_settings.DISABLE_TRIANGULATION, True)
tree_settings.set(tree_settings.DISABLE_OPENING_SUBTRACTIONS, True)
it = ifcopenshell.geom.iterator(tree_settings, ifc, include=("IfcSpace",))
t = ifcopenshell.geom.tree()
t.add_iterator(it)

# search tree
a = t.select(location, extend=0.4)
print(f'Door: {doors[0].Name} belongs to room {a[0].LongName}')
