from objects.geometricObject import Colour, GeometricObject, ObjectsList, VerticesList


class Wireframe(GeometricObject):
    """A Wireframe consists of multiple points in space"""
    def __init__(
        self,
        name: str,
        colour: Colour,
        vertices: VerticesList,
        obj_types: ObjectsList,
    ) -> None:
        """
        Creates a Wireframe object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param edges: A tuple of Coordinate tuples
        """
        if len(obj_types) < 2:
            raise ValueError("Wireframe requires more than 2 edges")

        super(Wireframe, self).__init__(name, "Wireframe", colour, vertices, obj_types)
