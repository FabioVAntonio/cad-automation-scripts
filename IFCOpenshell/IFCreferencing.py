import numpy as np
import math

import ifcopenshell
from ifcopenshell.util.placement import get_local_placement
from ifcopenshell.util.unit import calculate_unit_scale
import ifcopenshell, ifcopenshell.api as api


base_ifc_path = "C:/Users/fabio/OneDrive/Dokumente/Coding/cad-automation-scripts/IFCs, PLNs and RVTs/"
reference_ifc = ifcopenshell.open(base_ifc_path+"Test_reference.ifc")
reading_ifc = ifcopenshell.open(base_ifc_path+"Test_reading_rotated.ifc")

try:
    corrected_ifc = ifcopenshell.open(base_ifc_path+"Test_reading_rotated CORRECTED.ifc")
except:
    pass

def get_twin_element(reference_ifc, reading_ifc, searched_globalId: str) -> tuple:
    #set reference element (for example coordination pyramid)
    #given specific GlobalId, search it in reference_ifc
    #searched_globalId: 2OvmFKxZD5Kw$NbYjVKwpu -> index = 0 in reference_ifc

    for i in range(len(reference_ifc.by_type('IfcElement'))):
        reference_globalId = reference_ifc.by_type('IfcElement')[i].get_info().get("GlobalId")
        if reference_globalId == searched_globalId:
            reference_index = i

    #search in reading_ifc
    for i in range(len(reading_ifc.by_type('IfcElement'))):
        reading_globalId = reading_ifc.by_type('IfcElement')[i].get_info().get("GlobalId")
        if reading_globalId == searched_globalId:
            reading_index = i

    return reference_index, reading_index #maybe variable output? type of IFC, name, etc.

def get_twin_matrices(reference_ifc, reading_ifc, searched_globalId: str, short_matrix: bool) -> tuple:
    reference_index, reading_index = get_twin_element(reference_ifc, reading_ifc, searched_globalId)
    #get transformation T vector based on same element
    element = reference_ifc.by_type('IfcElement')[reference_index]
    reference_placement_matrix = get_local_placement(element.ObjectPlacement)

    element = reading_ifc.by_type('IfcElement')[reading_index]
    reading_placement_matrix = get_local_placement(element.ObjectPlacement)

    if short_matrix:
        return reference_placement_matrix[0:3,3], reading_placement_matrix[0:3,3]
    else:
        return reference_placement_matrix, reading_placement_matrix

    #calculate transformation T based on reading/reference matrix

def get_transformation_T(reference_ifc, reading_ifc, searched_globalId: str):
    reference_matrix, reading_matrix = get_twin_matrices(reference_ifc, reading_ifc, searched_globalId, short_matrix=False)

    return reference_matrix @ np.linalg.inv(reading_matrix)

def move_ifc(reference_ifc, reading_ifc, searched_globalId: str):
    T = get_transformation_T(reference_ifc, reading_ifc, searched_globalId)
    
    roots = reading_ifc.by_type("IfcBuildingStorey")

    for i, storey in enumerate(roots):
        M = ifcopenshell.util.placement.get_local_placement(storey.ObjectPlacement)
        # check if you need M @ T instead of T @ M
        new_M = T @ M
        api.run(
            "geometry.edit_object_placement",
            reading_ifc,
            product=storey,
            matrix=new_M,
            is_si=True, # set to False if T is in project units (e.g., mm)
            should_transform_children=True
        )

        print(f"Moved storey {i+1} out of {len(roots)}. Story: "+storey.get_info().get("Name"))

    new_IFC = "Test_reading_rotated CORRECTED.ifc"
    reading_ifc.write(base_ifc_path+new_IFC)
    print(f"Saved new IFC: {new_IFC}")

if __name__ == "__main__":
    move_ifc(reference_ifc, reading_ifc, searched_globalId="2OvmFKxZD5Kw$NbYjVKwpu")
    #print(get_transformation_T(reference_ifc, corrected_ifc, "2OvmFKxZD5Kw$NbYjVKwpu"))
    #print(get_twin_matrices(reference_ifc, corrected_ifc, "2OvmFKxZD5Kw$NbYjVKwpu", short_matrix=False))