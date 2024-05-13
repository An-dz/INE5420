from objects.geometricObject import Colour, GeometricObject, ObjectsList, VerticesList


class Object3D(GeometricObject):
    """A Wireframe consists of multiple points in space"""
    def __init__(
        self,
        name: str,
        colour: Colour,
        vertices: VerticesList,
        obj_types: ObjectsList,
    ) -> None:
        """
        Creates a 3D object

        @warn should not be called directly, use the object Factory instead

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param edges: A tuple of Coordinate tuples
        """
        super(Object3D, self).__init__(name, "Object3D", colour, vertices, obj_types)
