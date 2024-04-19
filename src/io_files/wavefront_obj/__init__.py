from pathlib import Path

from displayFile import DisplayFile
from io_files.wavefront_obj.mtllib import MaterialLibraryReader, MaterialLibraryWriter
from objects.factory import Factory
from objects.geometricObject import GeometricObject, NormalCoordinate, ObjectsList


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
            vertices: list[NormalCoordinate] = []
            object_name = "Imported"
            object_colour = (204, 204, 204)
            object_index = 0
            mtl_file = None
            object_types: ObjectsList = []

            for line in file:
                items = line.split()

                if items:
                    if len(object_types) > 0 and items[0] not in ["l", "f", "p"]:
                        objects.append(Factory.create_object(
                            object_name,
                            object_colour,
                            vertices,
                            object_types,
                        ))
                        object_types = []

                    #-----------------------------------------#
                    #               Vertex data               #
                    #-----------------------------------------#
                    if items[0] == "v":  # geometric vertices
                        vertices.append((float(items[1]), float(items[2]), 1))
                    # elif items[0] == "vt":  # texture vertices
                    # elif items[0] == "vn":  # vertex normals
                    # elif items[0] == "vp":  # parameter space vertices
                    #-----------------------------------------#
                    #                Elements                 #
                    #-----------------------------------------#
                    elif items[0] == "p":  # point
                        for i in range(1, len(items)):
                            object_index += 1
                            point = vertices[int(items[i].split("/")[0]) - 1]
                            object_types.append((point, ))
                    elif items[0] == "l":  # line
                        for i in range(2, len(items)):
                            object_types.append((
                                vertices[int(items[i - 1].split("/")[0]) - 1],
                                vertices[int(items[i].split("/")[0]) - 1],
                            ))
                    elif items[0] == "f":  # face
                        object_types.append(
                            tuple(
                                vertices[int(items[i].split("/")[0]) - 1]
                                for i in range(1, len(items))
                            ),
                        )
                    # elif items[0] == "curv":  # curve
                    # elif items[0] == "curv2":  # 2D curve
                    # elif items[0] == "surf":  # surface
                    #-----------------------------------------#
                    #    Free-form curve/surface attributes   #
                    #-----------------------------------------#
                    # elif items[0] == "cstype":
                    #     # rational or non-rational forms of curve or surface type:
                    #     # basis matrix, Bezier, B-spline, Cardinal, Taylor
                    # elif items[0] == "deg":  # degree
                    # elif items[0] == "bmat":  # basis matrix
                    # elif items[0] == "step":  # step size
                    #-----------------------------------------#
                    # Free-form curve/surface body statements #
                    #-----------------------------------------#
                    # elif items[0] == "parm":  # parameter values
                    # elif items[0] == "trim":  # outer trimming loop
                    # elif items[0] == "hole":  # inner trimming loop
                    # elif items[0] == "scrv":  # special curve
                    # elif items[0] == "sp":  # special point
                    # elif items[0] == "end":  # end statement
                    #-----------------------------------------#
                    # Connectivity between free-form surfaces #
                    #-----------------------------------------#
                    # elif items[0] == "con":  # connect
                    #-----------------------------------------#
                    #                Grouping                 #
                    #-----------------------------------------#
                    elif items[0] == "g":  # group name
                        pass
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
                    coords = obj.get_coordinates()
                    lazy_write.append("o {}\n".format(obj.get_name()))
                    material_name = mtl_file.write_material(obj.get_colour())
                    lazy_write.append("usemtl {}\n".format(material_name))
                    is_line = False

                    for coord in coords:
                        file.write("v {} {} 0.0\n".format(coord[0], coord[1]))
                        vertex_count += 1

                        if is_line:
                            lazy_write.append("l {} {}\n".format(
                                vertex_count - 1, vertex_count,
                            ))

                        is_line = True

                    if len(coords) == 1:
                        lazy_write.append("p {}\n".format(vertex_count))

                    lazy_write.append("\n")

                file.write("\n")

            for line in lazy_write:
                file.write(line)
