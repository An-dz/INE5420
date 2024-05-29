from pathlib import Path
from typing import Optional

import numpy as np

from displayFile import DisplayFile
from io_files.wavefront_obj.mtllib import MaterialLibraryReader, MaterialLibraryWriter
from objects.bezier_curve import BezierCurve
from objects.bezier_surface import BezierSurface
from objects.bspline_curve import BSplineCurve
from objects.bspline_surface import BSplineSurface
from objects.factory import Factory
from objects.geometricObject import Colour, Coordinate, GeometricObject, NormalCoordinate, ObjectsList


class WavefrontDescriptor:
    """Reader & Writer for Wavefront .obj"""

    @staticmethod
    def import_file(filepath: str) -> list[GeometricObject]:
        """
        Reads and imports a Wavefront OBJ scene file and its MTL files

        @param filepath: Path for the OBJ file to import

        @returns: List of Geometric Objects to add to the scene
        """
        if len(filepath) == 0:
            return []

        obj_filepath = Path(filepath)
        objects: list[GeometricObject] = []

        with open(obj_filepath) as file:
            vertices: list[NormalCoordinate] = [(0, 0, 0, 1)]
            object_vertices: list[NormalCoordinate] = []
            object_name = "Imported"
            object_colour = (204, 204, 204)
            object_index = 0
            mtl_file = None
            object_types: ObjectsList = []
            curve_importing: Optional[CurveImport] = None
            continue_vertices = False
            continue_parm: Optional[str] = None

            for line in file:
                items = line.split()

                if items:
                    if continue_vertices and curve_importing:
                        continue_vertices = False

                        for i in range(len(items)):
                            if items[i] != "\\":
                                curve_importing.add_point(vertices[int(items[i])])
                            else:
                                continue_vertices = True
                    elif continue_parm and curve_importing:
                        if items[-1] == "\\":
                            curve_importing.set_num_knots(continue_parm, len(items) - 1)
                        else:
                            curve_importing.set_num_knots(continue_parm, len(items))
                            continue_parm = None
                    elif (
                        curve_importing is None
                        and len(object_types) > 0
                        and items[0] not in ["l", "f", "p"]
                    ):
                        objects.append(Factory.create_object(
                            object_name,
                            object_colour,
                            object_vertices,
                            object_types,
                            False,
                        ))
                        object_types = []
                        object_vertices = []
                        object_name = "Imported"

                    #-----------------------------------------#
                    #               Vertex data               #
                    #-----------------------------------------#
                    if items[0] == "v":  # geometric vertices
                        vertices.append((
                            float(items[1]),
                            float(items[2]),
                            float(items[3]),
                            1,
                        ))
                    # elif items[0] == "vt":  # texture vertices
                    # elif items[0] == "vn":  # vertex normals
                    # elif items[0] == "vp":  # parameter space vertices
                    #-----------------------------------------#
                    #                Elements                 #
                    #-----------------------------------------#
                    elif items[0] == "p":  # point
                        for i in range(1, len(items)):
                            object_index += 1
                            point = vertices[int(items[i].split("/")[0])]
                            object_vertices.append(point)
                            object_types.append((point, ))
                    elif items[0] == "l":  # line
                        for i in range(2, len(items)):
                            point_a = vertices[int(items[i - 1].split("/")[0])]
                            point_b = vertices[int(items[i].split("/")[0])]
                            object_vertices.append(point_a)
                            object_vertices.append(point_b)
                            object_types.append((point_a, point_b))
                    elif items[0] == "f":  # face
                        for i in range(1, len(items)):
                            object_vertices.append(vertices[int(items[i].split("/")[0])])

                        object_types.append(
                            tuple(
                                vertices[int(items[i].split("/")[0])]
                                for i in range(1, len(items))
                            ),
                        )
                    elif items[0] == "curv":  # curve
                        if curve_importing is None:
                            continue
                        # skip u0 and u1
                        for i in range(3, len(items)):
                            if items[i] != "\\":
                                curve_importing.add_point(vertices[int(items[i])])
                            else:
                                continue_vertices = True
                    # elif items[0] == "curv2":  # 2D curve
                    elif items[0] == "surf":  # surface
                        if curve_importing is None:
                            continue

                        curve_importing.set_as_surface()
                        # skip s0, s1, t0 and t1
                        for i in range(5, len(items)):
                            if items[i] != "\\":
                                curve_importing.add_point(
                                    vertices[int(items[i].split("/")[0])],
                                )
                            else:
                                continue_vertices = True
                    #-----------------------------------------#
                    #    Free-form curve/surface attributes   #
                    #-----------------------------------------#
                    elif items[0] == "cstype":
                        # rational or non-rational forms of curve or surface type:
                        # basis matrix, Bezier, B-spline, Cardinal, Taylor
                        curve_type = items[1] if items[1] != "rat" else items[2]

                        if curve_type in ["bezier", "bspline"]:
                            curve_importing = CurveImport(curve_type)
                    elif items[0] == "deg":  # degree
                        if curve_importing is None:
                            continue

                        if len(items) == 3:
                            curve_importing.set_as_surface()
                            curve_importing.set_degrees(int(items[1]), int(items[2]))
                        else:
                            curve_importing.set_degrees(int(items[1]), 0)
                    # elif items[0] == "bmat":  # basis matrix
                    # elif items[0] == "step":  # step size
                    #-----------------------------------------#
                    # Free-form curve/surface body statements #
                    #-----------------------------------------#
                    elif items[0] == "parm":  # parameter values
                        if curve_importing is None:
                            continue

                        if items[-1] == "\\":
                            curve_importing.set_num_knots(items[1], len(items) - 3)
                            continue_parm = items[1]
                        else:
                            curve_importing.set_num_knots(items[1], len(items) - 2)
                    # elif items[0] == "trim":  # outer trimming loop
                    # elif items[0] == "hole":  # inner trimming loop
                    # elif items[0] == "scrv":  # special curve
                    # elif items[0] == "sp":  # special point
                    elif items[0] == "end":  # end statement
                        if curve_importing is None:
                            continue

                        curve = curve_importing.return_object(object_name, object_colour)

                        if curve:
                            objects.append(curve)

                        object_name = "Imported"
                        curve_importing = None
                    #-----------------------------------------#
                    # Connectivity between free-form surfaces #
                    #-----------------------------------------#
                    # elif items[0] == "con":  # connect
                    #-----------------------------------------#
                    #                Grouping                 #
                    #-----------------------------------------#
                    elif items[0] == "g":  # group name
                        object_name = items[1]
                    # elif items[0] == "s":  # smoothing group
                    # elif items[0] == "mg":  # merging group
                    elif items[0] == "o":  # object name
                        object_name = items[1]
                    #-----------------------------------------#
                    #        Display/render attributes        #
                    #-----------------------------------------#
                    # elif items[0] == "bevel":  # bevel interpolation
                    # elif items[0] == "c_interp":  # color interpolation
                    # elif items[0] == "d_interp":  # dissolve interpolation
                    # elif items[0] == "lod":  # level of detail
                    elif items[0] == "usemtl":  # material name
                        if mtl_file:
                            object_colour = mtl_file.get_material(items[1])
                            if object_colour is None:
                                object_colour = (204, 204, 204)
                    elif items[0] == "mtllib":  # material library
                        mtl_file = MaterialLibraryReader([
                            obj_filepath.with_name(item) for item in items[1:]
                        ])
                    # elif items[0] == "shadow_obj":  # shadow casting
                    # elif items[0] == "trace_obj":  # ray tracing
                    # elif items[0] == "ctech":  # curve approximation technique
                    # elif items[0] == "stech":  # surface approximation technique

        if len(object_types) > 0:
            objects.append(Factory.create_object(
                object_name,
                object_colour,
                vertices,
                object_types,
                False,
            ))

        return objects

    @staticmethod
    def export_file(filepath: str, display_file: DisplayFile) -> None:
        """
        @brief Writes a Wavefront OBJ scene file and
        its MTL file from the current display_file

        This will generate both an OBJ file and an MTL file

        @param filepath: Path for the OBJ file to import
        @param display_file: Display File holding the objects to export
        """
        if len(filepath) == 0:
            return

        obj_filepath = Path(filepath)
        mtl_filepath = obj_filepath.with_suffix(".mtl")

        if obj_filepath.suffix == "":
            obj_filepath = obj_filepath.with_suffix(".obj")

        with open(obj_filepath, "w") as file:
            file.write("# Bländär\n\nmtllib {}\n\n".format(mtl_filepath.name))
            vertex_count = 0
            lazy_write: list[str] = []

            with MaterialLibraryWriter(mtl_filepath) as mtl_file:
                for obj in display_file.objects():
                    obj_group = obj.get_coordinates()
                    vertices: list[Coordinate] = []

                    if isinstance(obj, BSplineSurface):
                        control_points = obj_group[0]
                        coords = control_points.reshape(
                            control_points.shape[0] * control_points.shape[1],
                            4,
                        )

                        for coord in coords:
                            file.write("v {:.6f} {:.6f} {:.6f}\n".format(
                                coord[0], coord[1], coord[2],
                            ))
                            vertex_count += 1

                        file.write("g {}\n".format(
                            obj.get_name().replace(" ", "_") or "BSpline"),
                        )
                        material_name = mtl_file.write_material(obj.get_colour())
                        file.write("usemtl {}\n".format(material_name))
                        file.write("cstype bspline\n")
                        file.write("deg 3 3\n")
                        file.write("surf 0.000000 1.000000 0.000000 1.000000 {}\n".format(
                            " ".join(
                                [
                                    "{}".format(i) for i in range(
                                        vertex_count - len(coords) + 1,
                                        vertex_count + 1,
                                    )
                                ],
                            ),
                        ))
                        # control points + degree (3) + 1
                        tot_parm = control_points.shape[0] + 4
                        tot_parm_div = float(tot_parm - 1)
                        parm_ls = [(i / tot_parm_div) for i in range(tot_parm)]
                        file.write("parm u {}\n".format(
                            " ".join(["{:.6f}".format(u) for u in parm_ls]),
                        ))
                        # control points + degree (3) + 1
                        tot_parm = control_points.shape[1] + 4
                        tot_parm_div = float(tot_parm - 1)
                        parm_ls = [(i / tot_parm_div) for i in range(tot_parm)]
                        file.write("parm v {}\n".format(
                            " ".join(["{:.6f}".format(v) for v in parm_ls]),
                        ))
                        file.write("end\n")

                        continue
                    elif isinstance(obj, BezierSurface):
                        coords = obj_group[0].reshape(16, 4)

                        for coord in coords:
                            file.write("v {:.6f} {:.6f} {:.6f}\n".format(
                                coord[0], coord[1], coord[2],
                            ))
                            vertex_count += 1

                        file.write("g {}\n".format(
                            obj.get_name().replace(" ", "_") or "Bezier"),
                        )
                        material_name = mtl_file.write_material(obj.get_colour())
                        file.write("usemtl {}\n".format(material_name))
                        file.write("cstype bezier\n")
                        file.write("deg 3 3\n")
                        file.write("surf 0.000000 1.000000 0.000000 1.000000 {}\n".format(
                            " ".join(
                                [
                                    "{}".format(c) for c in range(
                                        vertex_count - len(coords) + 1,
                                        vertex_count + 1,
                                    )
                                ],
                            ),
                        ))
                        file.write("parm u 0.000000 1.000000\n")
                        file.write("parm v 0.000000 1.000000\n")
                        file.write("end\n")

                        continue
                    elif isinstance(obj, BezierCurve):
                        coords = obj_group[0]

                        for coord in coords:
                            file.write("v {:.6f} {:.6f} {:.6f}\n".format(
                                coord[0], coord[1], coord[2],
                            ))
                            vertex_count += 1

                        file.write("g {}\n".format(
                            obj.get_name().replace(" ", "_") or "Bezier"),
                        )
                        material_name = mtl_file.write_material(obj.get_colour())
                        file.write("usemtl {}\n".format(material_name))
                        file.write("cstype bezier\n")
                        file.write("deg 3\n")
                        file.write("curv 0.000000 1.000000 {}\n".format(
                            " ".join(
                                [
                                    "{}".format(c) for c in range(
                                        vertex_count - len(coords) + 1,
                                        vertex_count + 1,
                                    )
                                ],
                            ),
                        ))
                        file.write("parm u 0.000000 1.000000\n")
                        file.write("end\n\n")

                        continue
                    elif isinstance(obj, BSplineCurve):  # surface inherits the curve
                        coords = obj_group[0]

                        for coord in coords:
                            file.write("v {:.6f} {:.6f} {:.6f}\n".format(
                                coord[0], coord[1], coord[2],
                            ))
                            vertex_count += 1

                        file.write("g {}\n".format(
                            obj.get_name().replace(" ", "_") or "BSpline"),
                        )
                        material_name = mtl_file.write_material(obj.get_colour())
                        file.write("usemtl {}\n".format(material_name))
                        file.write("cstype bspline\n")
                        file.write("deg 3\n")
                        file.write("curv 0.000000 1.000000 {}\n".format(
                            " ".join(
                                [
                                    "{}".format(c) for c in range(
                                        vertex_count - len(coords) + 1,
                                        vertex_count + 1,
                                    )
                                ],
                            ),
                        ))
                        tot_parm = len(coords) + 4  # control points + degree (3) + 1
                        tot_parm_div = float(tot_parm - 1)
                        parm_ls = [(i / tot_parm_div) for i in range(tot_parm)]
                        file.write("parm u {}\n".format(
                            " ".join(["{:.6f}".format(u) for u in parm_ls]),
                        ))
                        file.write("end\n\n")

                        continue

                    file.write("o {}\n".format(
                        obj.get_name().replace(" ", "_") or "Object"),
                    )

                    for obj_coords in obj_group:
                        item_vertices: list[int] = []

                        for coord in obj_coords:
                            vertex = (coord[0], coord[1], coord[2])

                            if vertex not in vertices:
                                vertices.append(vertex)
                                file.write("v {:.6f} {:.6f} {:.6f}\n".format(*vertex))
                                vertex_count += 1
                                item_vertices.append(vertex_count)
                            else:
                                item_vertices.append(
                                    vertex_count - len(vertices)
                                    + vertices.index(vertex) + 1,
                                )

                        if len(item_vertices) == 1:
                            lazy_write.append("p {}\n".format(item_vertices[0]))
                        elif len(item_vertices) == 2:
                            lazy_write.append("l {} {}\n".format(
                                item_vertices[0],
                                item_vertices[1],
                            ))
                        else:
                            lazy_write.append("f {}".format(
                                " ".join(["{}".format(i) for i in item_vertices]),
                            ))

                    material_name = mtl_file.write_material(obj.get_colour())
                    file.write("usemtl {}\n".format(material_name))

                    for line in lazy_write:
                        file.write(line)

                    lazy_write = []
                    file.write("\n")


class CurveImport:
    """docstring for CurveImport"""
    def __init__(self, curve_type: str) -> None:
        self._type = curve_type
        self._points: list[NormalCoordinate] = []
        self._surface = False
        self._degrees = (0, 0)
        self._knots = {
            "u": 0,
            "v": 0,
        }

    def return_object(self, name: str, colour: Colour) -> Optional[GeometricObject]:
        try:
            if self._surface:
                if self._type == "bezier":
                    return BezierSurface(name, colour, self._points)

                return BSplineSurface(
                    name,
                    colour,
                    np.array(self._points).reshape(
                        # control points = knots - degreee - 1
                        self._knots["u"] - self._degrees[0] - 1,
                        self._knots["v"] - self._degrees[1] - 1,
                        4,
                    ),
                )

            return Factory.create_object(
                name,
                colour,
                self._points,
                [],
                self._type == "bspline",
            )
        except Exception:
            return None

    def add_point(self, vertice: NormalCoordinate) -> None:
        self._points.append(vertice)

    def set_as_surface(self) -> None:
        self._surface = True

    def set_degrees(self, u_deg: int, v_deg: int) -> None:
        self._degrees = (u_deg, v_deg)

    def set_num_knots(self, axis: str, amount: int) -> None:
        self._knots[axis] += amount
