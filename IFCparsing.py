import time
#-----starts time-----#
start = time.time()


# testing IFCOpenshell
import multiprocessing
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
from ifcopenshell.util.selector import Selector
from ifcopenshell.util.placement import get_local_placement


ifc_Test = ifcopenshell.open('./IFCs, PLNs and RVTs/Test.ifc')
ifc_Test_new = ifcopenshell.open('./IFCs, PLNs and RVTs/Test (new).ifc')
ifc_objects = ifcopenshell.open('./IFCs, PLNs and RVTs/Objects.ifc')
selector = Selector()



wall = ifc_Test.by_type('IfcWall')[0]
zones = ifc_Test.by_type('IfcSpace')
zone = ifc_Test.by_type('IfcSpace')[0]
doors = ifc_Test.by_type('IfcDoor')

object = ifc_objects.by_type('IfcFurniture')
test_objects = ifc_Test.by_type('IfcFurniture')

#print(wall.get_info())      #gets: id , type, GlobalId, OwnerHistory, Name, etc.. in key/value pairs
#print(wall.get_info().get('Name'))  #pick out specific info  or in short: print(wall.Name)
#zones[0].Name = test  --> overwrites room number

#placement_matrix = get_local_placement(test_objects[-2].ObjectPlacement)
#print(placement_matrix)

#test_objects[-2] = object   #changing of objects

#ifc = ifc.write('./IFCs and PLNs/Test.ifc')    #overwrites current IFC file

#elements = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')
#elements_2 = selector.parse(ifc, '@@ .IfcSpace & ( .IfcDoor  )')[4]

location = ()
#location of door[0] (as an example) with its nearest IfcSpace
def matrix(element, i):
    global location
    matrix = get_local_placement(element[i].ObjectPlacement)
    location = tuple(map(float, matrix[0:3,3]))
    return location

def decision_tree(element, i):
    matrix(element, i)
    tree_settings = ifcopenshell.geom.settings()
    tree_settings.set(tree_settings.DISABLE_TRIANGULATION, True)
    tree_settings.set(tree_settings.DISABLE_OPENING_SUBTRACTIONS, True)
    it = ifcopenshell.geom.iterator(tree_settings, ifc_Test, include=("IfcSpace",))
    t = ifcopenshell.geom.tree()
    t.add_iterator(it)

    # search tree
    a = t.select(location, extend=0.4)
    print(f'Door: {element[i].Name}  belongs to  {a[1].Name}: {a[1].LongName}\n')
    print(a)

#decision_tree(doors, 5) #Door: 1.02 T01  belongs to  WE 1.02: Bad_M ... a[1] (index is deviant)


def renaming(): #make it input based for multiple elements
    print(doors[0].get_info())
    print(f"Original name: {doors[0].Name}")
    doors[0].Name = "Test"
    print(f"Renaming: SUCCESSFUL")

    ifc_Test.write('./IFCs, PLNs and RVTs/Test (new).ifc')
    print("Saving: SUCCESSFUL")

    doors_new = ifc_Test_new.by_type('IfcDoor')
    print(f"New name: {doors_new[0].Name}")

renaming()


#-----stops time-----#
end = time.time()
print('Runtime is:', (end-start) * 1, 's')