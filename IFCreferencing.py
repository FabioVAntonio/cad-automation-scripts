import ifcopenshell
from ifcopenshell.util.selector import Selector
from ifcopenshell.util.placement import get_local_placement

import numpy as np

reference_ifc = ifcopenshell.open('./IFCs, PLNs and RVTs/Test_reference.ifc')
reading_ifc = ifcopenshell.open('./IFCs, PLNs and RVTs/Test_reading.ifc')

wall = reference_ifc.by_type('IfcWall')[0]


def get_associative_element(searched_globalId: str) -> int:
    #set reference element (for example coordination pyramid)
    #given specific GlobalId, search it in reference_ifc
    #searched_globalId: 2OvmFKxZD5Kw$NbYjVKwpu -> index = 0 in reference_ifc

    for i in range(len(reference_ifc.by_type('IfcWall'))):
        reference_globalId = reference_ifc.by_type('IfcWall')[i].get_info().get("GlobalId")
        if reference_globalId == searched_globalId:
            reference_index = i

    #search in reading_ifc
    for i in range(len(reading_ifc.by_type('IfcWall'))):
        reading_globalId = reading_ifc.by_type('IfcWall')[i].get_info().get("GlobalId")
        if reading_globalId == searched_globalId:
            reading_index = i

    return [reference_index, reading_index] #maybe variable output? type of IFC, name, etc.

def get_transformation_T(searched_globalId: str) -> tuple:
    reference_index, reading_index = get_associative_element(searched_globalId)
    #get transformation T vector based on same element
    wall = reference_ifc.by_type('IfcWall')[reference_index]
    reference_placement_matrix = get_local_placement(wall.ObjectPlacement)

    wall = reading_ifc.by_type('IfcWall')[reading_index]
    reading_placement_matrix = get_local_placement(wall.ObjectPlacement)
    return reference_placement_matrix, reading_placement_matrix

def get_rotation_R():
    pass

def transform_ifc():

    transformed_ifc = reading_ifc.write('./IFCs and PLNs/Test_transformed.ifc')

if __name__ == "__main__":
    print(get_transformation_T("2OvmFKxZD5Kw$NbYjVKwpu"))
