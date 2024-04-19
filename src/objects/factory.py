from objects.geometricObject import Colour, GeometricObject, ObjectsList, VerticesList
from objects.line import Line
from objects.point import Point
from objects.polygon import Polygon
from objects.wireframe import Wireframe


class Factory:
    """Simple factory for generating the correct type of object based on input"""
    @staticmethod
    def create_object(
        name: str,
        colour: Colour,
        vertices: VerticesList,
        obj_types: ObjectsList,
    ) -> GeometricObject:
        """
        Creates an appropriate geometric object according to the amount of points given

        @param name: A name to show in the object list
        @param colour: A colour to draw the object
        @param points: A list of line segments,
        if the initial and final points are equal its a point
        """
        obj_amount = len(obj_types)
        coord_amount = len(obj_types[0])
        if obj_amount == 1 and coord_amount == 1:
            return Point(name, colour, obj_types[0][0])

        if obj_amount == 1 and coord_amount == 2:
            return Line(name, colour, obj_types[0][0], obj_types[0][1])

        for obj in obj_types:
            if len(obj) > 2:
                return Polygon(name, colour, vertices, obj_types)

        return Wireframe(name, colour, vertices, obj_types)
