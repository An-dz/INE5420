from objects.geometricObject import Colour, GeometricObject, ObjectsList, VerticesList


class Polygon(GeometricObject):
    """A Polygon consists of a hamiltonian graph wireframe but filled"""
    def __init__(
        self,
        name: str,
        colour: Colour,
        vertices: VerticesList,
        obj_types: ObjectsList,
    ) -> None:
        """
        Creates a Polygon object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param edges: A tuple of Coordinate tuples
        """
        super(Polygon, self).__init__(name, "Polygon", colour, vertices, obj_types)
