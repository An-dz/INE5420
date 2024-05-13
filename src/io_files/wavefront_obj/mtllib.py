from pathlib import Path
from typing import Literal

from objects.geometricObject import Colour


class MaterialLibraryReader:
    """Read material data from multiple MTL files"""
    def __init__(self, filepaths: list[Path]) -> None:
        """
        Reads a list of MTL files and extracts the
        material data to be used by an OBJ scene

        @param filepaths: List of paths to MTL files in order of precedence,
        where the first on the list take precedence
        """
        self._filepaths = filepaths
        self._materials: dict[str, Colour] = {}

        # we reverse as the first paths take precedence
        for filepath in reversed(self._filepaths):
            with open(filepath) as file:
                cur_material = ""

                for line in file:
                    items = line.split()

                    if items:
                        if items[0] == "newmtl":  # new material defined
                            cur_material = items[1]
                        # if items[0] == "Ka":  # ambient color / default is (0.2,0.2,0.2)
                        elif items[0] == "Kd":  # diffuse color / default is (0.8,0.8,0.8)
                            self._materials[cur_material] = (
                                round(float(items[1]) * 255),
                                round(float(items[2]) * 255),
                                round(float(items[3]) * 255),
                            )
                        # elif items[0] == "Ks":  # specular color / default is (1,1,1)
                        # elif items[0] == "d":  # non-transparency alpha / default is 1.0
                        # elif items[0] == "Tr":  # transparency alpha / default is 0.0
                        # elif items[0] == "Ns":  # shininess / The default is 0.0
                        # elif items[0] == "illum":  # illumination model
                        # elif items[0] == "map_Ka":  # file containing texture map

    def get_material(self, name: str) -> Colour | None:
        """
        @brief Obtain the colour by material name

        After the MTL files have been read this allows
        extracting their colours by their material names

        @param name: Name of the material to obtain the colour

        @returns: Colour of the material or None if material is not registered
        """
        return self._materials.get(name)


class MaterialLibraryWriter:
    """Writer for a MTL file that holds material data"""
    def __init__(self, filepath: Path) -> None:
        """
        Write a new MTL file

        @param filepath: Path to save the MTL file
        """
        self._filepath = filepath
        self._colours: dict[str, str] = {}
        self._material_index = 0

    def __enter__(self) -> "MaterialLibraryWriter":
        """
        Opens the file once we enter the `with` statement and writes the header
        """
        self._file = open(self._filepath, "w")
        self._file.write("# Bländär MTL File\n\n")

        return self

    def __exit__(self, *_) -> Literal[False]:
        """
        Closes the file once we leave the `with` statement
        """
        self._file.close()
        return False

    def write_material(self, colour: Colour) -> str:
        """
        Write a new material to the MTL file and returns its name

        @warn: Make sure you opened the file with `with` statement or it will crash

        @note: Duplicate colours are merged into a single material

        @param colour: The colour to save in the MTL file

        @returns: Material name for that colour
        """
        colour_index = str(colour)
        material_name = self._colours.get(colour_index)

        if material_name is None:
            material_name = "Material{}".format(
                ".{:0>3}".format(
                    self._material_index,
                ) if self._material_index > 0 else "",
            )
            self._colours[colour_index] = material_name
            self._file.write("newmtl {}\nKd {:.6f} {:.6f} {:.6f}\n\n".format(
                material_name,
                colour[0] / 255,
                colour[1] / 255,
                colour[2] / 255,
            ))
            self._material_index += 1

        return material_name
