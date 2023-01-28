# testing IFCOpenshell
from fileinput import filename
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.pset






ifc = ifcopenshell.open('C:/Users/fabio/OneDrive/Dokumente/Coding/IFCnAPI Project/IFCs and PLNs/Test K1.ifc')
wall = ifc.by_type('IfcDoor')[0]
print(wall)


