# Copyright (c) [2024-2025] [Laszlo Oroszlany, Daniel Pozsar]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Visualization functions
=======================

.. currentmodule:: grogupy.io.io

.. autosummary::
   :toctree: _generated/

   load_DefaultTimer
   load_Contour
   load_Kspace
   load_MagneticEntity
   load_Pair
   load_Hamiltonian
   load_Builder
   load
   save
   save_magnopy
   read_magnopy
   read_fdf

"""
import importlib.util
import pickle
from os.path import join
from types import ModuleType
from typing import Union

import numpy as np
import sisl

from ..batch.timing import DefaultTimer
from ..physics.builder import Builder
from ..physics.contour import Contour
from ..physics.hamiltonian import Hamiltonian
from ..physics.kspace import Kspace
from ..physics.magnetic_entity import MagneticEntity
from ..physics.pair import Pair
from .utilities import strip_dict_structure


def load_DefaultTimer(infile: Union[str, dict]) -> DefaultTimer:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    DefaultTimer
        The DefaultTimer instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(DefaultTimer)
    out.__setstate__(infile)

    return out


def load_Contour(infile: Union[str, dict]) -> Contour:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    Contour
        The Contour instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(Contour)
    out.__setstate__(infile)

    return out


def load_Kspace(infile: Union[str, dict]) -> Kspace:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    Kspace
        The Kspace instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(Kspace)
    out.__setstate__(infile)

    return out


def load_MagneticEntity(infile: Union[str, dict]) -> MagneticEntity:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    MagneticEntity
        The MagneticEntity instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(MagneticEntity)
    out.__setstate__(infile)

    return out


def load_Pair(infile: Union[str, dict]) -> Pair:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    Pair
        The Pair instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(Pair)
    out.__setstate__(infile)

    return out


def load_Hamiltonian(infile: Union[str, dict]) -> Hamiltonian:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    Hamiltonian
        The Hamiltonian instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(Hamiltonian)
    out.__setstate__(infile)

    return out


def load_Builder(infile: Union[str, dict]) -> Builder:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    Builder
        The Builder instance that was loaded
    """

    # load pickled file
    if isinstance(infile, str):
        try:
            with open(infile, "rb") as file:
                infile = pickle.load(file)
        except:
            with open(infile + ".pkl", "rb") as file:
                infile = pickle.load(file)

    # build instance
    out = object.__new__(Builder)
    out.__setstate__(infile)

    return out


def load(
    infile: Union[str, dict]
) -> Union[DefaultTimer, Contour, Kspace, MagneticEntity, Pair, Hamiltonian, Builder]:
    """Recreates the instance from a pickled state.

    Parameters
    ----------
    infile : Union[str, dict]
        Either the path to the file or the appropriate
        dictionary for the setup

    Returns
    -------
    Union[DefaultTimer, Contour, Kspace, MagneticEntity, Pair, Hamiltonian, Builder]
        The instance that was loaded
    """
    # load pickled file
    if isinstance(infile, str):
        if not infile.endswith(".pkl"):
            infile += ".pkl"
        with open(infile, "rb") as file:
            infile = pickle.load(file)

    if list(infile.keys()) == [
        "times",
        "kspace",
        "contour",
        "hamiltonian",
        "magnetic_entities",
        "pairs",
        "_Builder__low_memory_mode",
        "_Builder__greens_function_solver",
        "_Builder__parallel_mode",
        "_Builder__architecture",
        "_Builder__matlabmode",
        "_Builder__exchange_solver",
        "_Builder__anisotropy_solver",
        "ref_xcf_orientations",
        "_rotated_hamiltonians",
        "SLURM_ID",
        "_Builder__version",
    ]:
        return load_Builder(infile)

    elif list(infile.keys()) == [
        "times",
        "_dh",
        "_ds",
        "infile",
        "_spin_state",
        "H",
        "S",
        "scf_xcf_orientation",
        "orientation",
        "_Hamiltonian__no",
        "hTRS",
        "hTRB",
        "XCF",
        "H_XCF",
        "_Hamiltonian__cell",
        "_Hamiltonian__sc_off",
        "_Hamiltonian__uc_in_sc_index",
    ]:
        return load_Hamiltonian(infile)
    elif list(infile.keys()) == [
        "_dh",
        "M1",
        "M2",
        "supercell_shift",
        "_Gij",
        "_Gji",
        "energies",
        "J_iso",
        "J",
        "J_S",
        "D",
        "_Pair__SBS1",
        "_Pair__SBS2",
        "_Pair__SBI1",
        "_Pair__SBI2",
        "_Pair__tags",
        "_Pair__cell",
        "_Pair__supercell_shift_xyz",
        "_Pair__xyz",
        "_Pair__xyz_center",
        "_Pair__distance",
        "_Pair__energies_meV",
        "_Pair__energies_mRy",
        "_Pair__J_meV",
        "_Pair__J_mRy",
        "_Pair__D_meV",
        "_Pair__D_mRy",
        "_Pair__J_S_meV",
        "_Pair__J_S_mRy",
        "_Pair__J_iso_meV",
        "_Pair__J_iso_mRy",
    ]:
        return load_Pair(infile)
    elif list(infile.keys()) == [
        "_dh",
        "_ds",
        "infile",
        "_atom",
        "_l",
        "_orbital_box_indices",
        "_tags",
        "_total_mulliken",
        "_local_mulliken",
        "_spin_box_indices",
        "_xyz",
        "_Vu1",
        "_Vu2",
        "_Gii",
        "energies",
        "K",
        "K_consistency",
        "_MagneticEntity__tag",
        "_MagneticEntity__SBS",
        "_MagneticEntity__xyz_center",
        "_MagneticEntity__total_Q",
        "_MagneticEntity__total_Sx",
        "_MagneticEntity__total_Sy",
        "_MagneticEntity__total_Sz",
        "_MagneticEntity__local_Q",
        "_MagneticEntity__local_Sx",
        "_MagneticEntity__local_Sy",
        "_MagneticEntity__local_Sz",
        "_MagneticEntity__energies_meV",
        "_MagneticEntity__energies_mRy",
        "_MagneticEntity__K_meV",
        "_MagneticEntity__K_mRy",
        "_MagneticEntity__K_consistency_meV",
        "_MagneticEntity__K_consistency_mRy",
    ]:
        return load_MagneticEntity(infile)
    elif list(infile.keys()) == ["times", "_Kspace__kset", "kpoints", "weights"]:
        return load_Kspace(infile)
    elif list(infile.keys()) == [
        "times",
        "_Contour__automatic_emin",
        "_eigfile",
        "_emin",
        "_emax",
        "_eset",
        "_esetp",
        "samples",
        "weights",
    ]:
        return load_Contour(infile)
    elif list(infile.keys()) == ["_DefaultTimer__start_measure", "_times"]:
        return load_DefaultTimer(infile)
    else:
        raise Exception("Unknown pickle format!")


def save(
    object: Union[
        DefaultTimer, Contour, Kspace, MagneticEntity, Pair, Hamiltonian, Builder
    ],
    path: str,
    compress: int = 3,
) -> None:
    """Saves the instance from a pickled state.

    The compression level can be set to 0,1,2,3. Every other value defaults to 3.

    0. This means that there is no compression at all.

    1. This means, that the keys "_dh" and "_ds" are set
       to None, because othervise the loading would be dependent
       on the sisl version

    2. This contains compression 1, but sets the keys "Gii",
       "Gij", "Gji",
       "Vu1" and "Vu2" to [], to save space

    3. This contains compression 1 and 2, but sets the keys
       "hTRS", "hTRB", "XCF" and "H_XCF" to None, to save space

    Parameters
    ----------
    object : Union[DefaultTimer, Contour, Kspace, MagneticEntity, Pair, Hamiltonian, Builder]
        Object from the grogupy library
    path: str
        The path to the output file
    compress: int, optional
        The level of lossy compression of the output pickle, by default 3
    """

    # check if the object is ours
    if object.__module__.split(".")[0] == "grogupy":
        # add pkl so we know it is pickled
        if not path.endswith(".pkl"):
            path += ".pkl"

        # the dictionary to be saved
        out_dict = object.__getstate__()

        # remove large objects to save memory or to avoid sisl loading errors
        if compress == 0:
            pass
        elif compress == 1:
            out_dict = strip_dict_structure(out_dict, pops=["_dh", "_ds"], setto=None)
        elif compress == 2:
            out_dict = strip_dict_structure(out_dict, pops=["_dh", "_ds"], setto=None)
            out_dict = strip_dict_structure(
                out_dict,
                pops=[
                    "_Gii",
                    "_Gij",
                    "_Gji",
                    "_Vu1",
                    "_Vu2",
                ],
                setto=[],
            )
        # compress 3 is the default
        else:
            out_dict = strip_dict_structure(out_dict, pops=["_dh", "_ds"], setto=None)
            out_dict = strip_dict_structure(
                out_dict,
                pops=[
                    "_Gii",
                    "_Gij",
                    "_Gji",
                    "_Vu1",
                    "_Vu2",
                ],
                setto=[],
            )
            out_dict = strip_dict_structure(
                out_dict, pops=["hTRS", "hTRB", "XCF", "H_XCF"], setto=None
            )

        # write to file
        with open(path, "wb") as f:
            pickle.dump(out_dict, f)

    else:
        raise Exception(
            f"The object is from package {object.__module__.split('.')[0]} instead of grogupy!"
        )


def save_UppASD(builder: Builder, folder: str, magnetic_moment: str = "total"):
    """Writes the UppASD input files to the given folder.

    The created input files are the posfile, momfile and
    jfile. Furthermore a cell.tmp.txt file is created which
    contains the unit cell for easy copy pasting.

    Parameters
    ----------
    builder : Builder
        Main simulation object containing all the data
    folder : str
        The out put folder where the files are created
    magnetic_moment: str, optional
        It switches the used spin moment in the output, can be 'total'
        for the whole atom or atoms involved in the magnetic entity or
        'local' if we only use the part of the mulliken projections that
        are exactly on the magnetic entity, which may be just a subshell
        of the atom, by default 'total'
    """
    posfile = ""
    momfile = ""
    # iterating over magnetic entities
    for i, mag_ent in enumerate(builder.magnetic_entities):
        # calculating positions in basis vector coordinates
        basis_vector_coords = mag_ent.xyz_center @ np.linalg.inv(mag_ent._dh.cell)
        bvc = np.around(basis_vector_coords, decimals=5)
        # adding line to posfile
        posfile += f"{i+1} {i+1} {bvc[0]:.5f} {bvc[1]:.5f} {bvc[2]:.5f}\n"

        # if magnetic moment is local
        if magnetic_moment.lower() == "l":
            S = np.array([mag_ent.local_Sx, mag_ent.local_Sy, mag_ent.local_Sz])
        # if magnetic moment is total
        else:
            S = np.array([mag_ent.total_Sx, mag_ent.total_Sy, mag_ent.total_Sz])
        # get the norm of the vector
        S_abs = np.linalg.norm(S)
        S = S / S_abs
        S = np.around(S, decimals=5)
        S_abs = np.around(S_abs, decimals=5)
        # adding line to momfile
        momfile += f"{i+1} 1 {S_abs:.5f} {S[0]:.5f} {S[1]:.5f} {S[2]:.5f}\n"

    jfile = ""
    # iterating over pairs
    for pair in builder.pairs:
        # iterating over magnetic entities and comparing them to the ones stored in the pairs
        for i, mag_ent in enumerate(builder.magnetic_entities):
            if mag_ent == pair.M1:
                ai = i
            if mag_ent == pair.M2:
                aj = i
        # this is the unit cell shift
        shift = pair.supercell_shift
        # -2 for convention, from Marci
        J = np.around(-2 * pair.J_mRy.flatten(), decimals=5)
        # adding line to jfile
        jfile += (
            f"{ai} {aj} {shift[0]} {shift[1]} {shift[2]} "
            + " ".join(map(lambda x: f"{x:.5f}", J))
            + "\n"
        )

    # cell as easily copy pastable string
    c = np.around(mag_ent._dh.cell, 5)
    string = f"{c[0,0]} {c[0,1]} {c[0,2]}\n{c[1,0]} {c[1,1]} {c[1,2]}\n{c[2,0]} {c[2,1]} {c[2,2]}"

    # writing them to the given folder
    with open(join(folder, "cell.tmp.txt"), "w") as f:
        print(string, file=f)
    with open(join(folder, "jfile"), "w") as f:
        print(jfile, file=f)
    with open(join(folder, "momfile"), "w") as f:
        print(momfile, file=f)
    with open(join(folder, "posfile"), "w") as f:
        print(posfile, file=f)


def save_magnopy(
    builder: Builder,
    path: str,
    magnetic_moment: str = "total",
    precision: Union[None, int] = None,
    comments: bool = True,
) -> None:
    """Creates a magnopy input file based on a path.

    It does not create the folder structure if the path is invalid.
    It saves to the outfile.

    Parameters
    ----------
    builder: Builder
        The system that we want to save
    path: str
        Output path
    magnetic_moment: str, optional
        It switches the used magnetic moment in the output, can be 'total'
        for the whole atom or atoms involved in the magnetic entity or
        'local' if we only use the part of the mulliken projections that
        are exactly on the magnetic entity, which may be just a subshell
        of the atom, by default 'total'
    precision: Union[None, int], optional
        The precision of the magnetic parameters in the output, if None
        everything is written, by default None
    comments: bool
        Wether to add comments in the beginning of file, by default True
    """

    if not path.endswith(".magnopy.txt"):
        path += ".magnopy.txt"

    data = builder.to_magnopy(
        magnetic_moment=magnetic_moment, precision=precision, comments=comments
    )
    with open(path, "w") as file:
        file.write(data)


def read_magnopy(file: str):
    """This function reads the magnopy input file and return a dictionary

    The dictionary contains sub-dictionaries with the section names and
    all of those sections contains a unit. Furthermore, because the main
    use of this function is to parse for magnetic entities and pair
    information it does that in the appropriate sections under the
    ``magnetic_entity`` and ``pairs`` keywords.

    Parameters
    ----------
    file: str
        Path to the ``magnopy`` input file

    Returns
    -------
    dict
        The dictionary containing all the information from the ``magnopy`` file

    Raises
    ------
    Exception
        If the unit for cell is not recognized
    Exception
        If the unit for atom is not recognized
    Exception
        If the unit for exchange is not recognized
    Exception
        If the unit for on-site is not recognized
    """

    with open(file, "r") as file:
        # select which sections and lines to parse
        lines = file.readlines()

    out: dict = dict()
    section = None
    pair = None
    full_matrix = 0
    for line in lines:
        # remove comments from line
        comment = line.find("#")
        line = line[:comment]
        # check for empty line
        if len(line.split()) == 0:
            continue

        # if we are in the matrix of a pair we have to read the next couple of lines
        if full_matrix > 0:
            if full_matrix == 3:
                pair["J"] = np.empty((3, 3))
                pair["J"][0] = np.array(line.split(), dtype=float)
            elif full_matrix == 2:
                pair["J"][1] = np.array(line.split(), dtype=float)
            elif full_matrix == 1:
                pair["J"][2] = np.array(line.split(), dtype=float)
            # the row is read, continue
            full_matrix -= 1
            continue

        # if section is not set, look for sections
        elif section is None:
            unit = None
            if line.split()[0].lower() == "cell":
                section = "cell"
                # unit is given
                if len(line.split()) > 1:
                    # only the first letter is checked and it is case-insensitive
                    unit = line.split()[1][0].lower()
                    if unit not in {"a", "b"}:
                        raise Exception("Unknown unit for cell")
                else:
                    unit = "a"

                # create cell part in the dictionary
                out["cell"] = dict()
                out["cell"]["unit"] = unit

            elif line.split()[0].lower() == "atoms":
                section = "atoms"
                # unit is given
                if len(line.split()) > 1:
                    # only the first letter is checked and it is case-insensitive
                    unit = line.split()[1][0].lower()
                    if unit not in {"a", "b"}:
                        raise Exception("Unknown unit for atoms")
                else:
                    unit = "a"

                # create cell part in the dictionary
                out["atoms"] = dict()
                out["atoms"]["unit"] = unit
                out["atoms"]["magnetic_entities"] = []

            elif line.split()[0].lower() == "notation":
                section = "notation"
                unit = None

            elif line.split()[0].lower() == "exchange":
                section = "exchange"
                # unit is given
                if len(line.split()) > 1:
                    # only the first letter is checked and it is case-insensitive
                    unit = line.split()[1][0].lower()
                    if unit not in {"m", "e", "j", "k", "r"}:
                        raise Exception("Unknown unit for exchange")
                else:
                    unit = "m"

                # create cell part in the dictionary
                out["exchange"] = dict()
                out["exchange"]["unit"] = unit
                out["exchange"]["pairs"] = []

            elif line.split()[0].lower() == "on-site":
                section = "on-site"
                # unit is given
                if len(line.split()) > 1:
                    # only the first letter is checked and it is case-insensitive
                    unit = line.split()[1][0].lower()
                    if unit not in {"m", "e", "j", "k", "r"}:
                        raise Exception("Unknown unit for on-site")
                else:
                    unit = "m"

                # create cell part in the dictionary
                out["on-site"] = dict()
                out["on-site"]["unit"] = unit
                out["on-site"]["magnetic_entities"] = []

            # we parsed the line
            continue

        # if section separator found set section for None
        if line[:10] == "==========":
            section = None
            atom = None
            pair = None
            continue

        # these are not needed for pair information
        if section == "cell":
            continue
        elif section == "notation":
            continue
        elif section == "on-site":
            if line[:10] == "----------":
                if atom is None:
                    continue
                else:
                    out["on-site"]["magnetic_entities"].append(atom)
                    atom = None

            elif len(line.split()) == 1:
                atom = dict(tag=line.split()[0])

            elif len(line.split()) == 6:
                atom["K"] = np.array([float(i) for i in line.split()])

        # these are needed for pair information
        # magnetic entities
        elif section == "atoms":
            # the name line
            if line.split()[0].lower() == "name":
                x_pos = np.where([word == "x" for word in line.split()])
                y_pos = np.where([word == "y" for word in line.split()])
                z_pos = np.where([word == "z" for word in line.split()])
            # magnetic entity line
            else:
                tag = line.split()[0]
                x = float(np.array(line.split())[x_pos])
                y = float(np.array(line.split())[y_pos])
                z = float(np.array(line.split())[z_pos])

                atom = dict(tag=tag, xyz=np.array([x, y, z]))
                out["atoms"]["magnetic_entities"].append(atom)

        elif section == "exchange":
            if line[:10] == "----------":
                if pair is None:
                    continue
                else:
                    out["exchange"]["pairs"].append(pair)
                    pair = None

            # isotropic keyword
            elif line.split()[0][0].lower() == "i":
                pair["iso"] = float(line.split()[1])

            # Dzyaloshinskii-Morilla keyword
            elif line.split()[0][0].lower() == "d":
                dx = float(line.split()[1])
                dy = float(line.split()[2])
                dz = float(line.split()[3])
                pair["DM"] = np.array([dx, dy, dz])

            # symmetric-anisotropy keyword
            elif line.split()[0][0].lower() == "s":
                sxx = float(line.split()[1])
                syy = float(line.split()[2])
                sxy = float(line.split()[3])
                sxz = float(line.split()[4])
                syz = float(line.split()[5])
                pair["S"] = np.array([sxx, syy, sxy, sxz, syz])

            # full matrix
            elif line.split()[0][0].lower() == "m":
                # this will avoid the whole loop and force to read the next 3 rows
                full_matrix = 3

            # tags and unit cell shift
            else:
                pair = dict()
                pair["tag1"] = line.split()[0]
                pair["tag2"] = line.split()[1]
                i = int(line.split()[2])
                j = int(line.split()[3])
                k = int(line.split()[4])

                pair["Ruc"] = np.array([i, j, k])

        else:
            continue

    for pair in out["exchange"]["pairs"]:
        for i, mag_ent in enumerate(out["atoms"]["magnetic_entities"]):
            if pair["tag1"] == mag_ent["tag"]:
                pair["xyz1"] = mag_ent["xyz"]
            if pair["tag2"] == mag_ent["tag"]:
                pair["xyz2"] = mag_ent["xyz"]

    return out


def read_fdf(path: str) -> tuple[dict, list, list]:
    """It reads the simulation parameters, magnetic entities and pairs from the fdf

    Parameters
    ----------
        path: str
            The path to the .fdf file

    Returns
    -------
        fdf_arguments: dict
            The read input arguments from the fdf file
        magnetic_entities: list
            It contains the dictionaries associated with the magnetic entities
        pairs: list
            It contains the dictionaries associated with the pair information
    """

    # read fdf file
    fdf = sisl.io.fdfSileSiesta(path)
    fdf_arguments = dict()

    InputFile = fdf.get("InputFile")
    if InputFile is not None:
        fdf_arguments["infile"] = InputFile

    OutputFile = fdf.get("OutputFile")
    if OutputFile is not None:
        fdf_arguments["outfile"] = OutputFile

    ScfXcfOrientation = fdf.get("ScfXcfOrientation")
    if ScfXcfOrientation is not None:
        fdf_arguments["scf_xcf_orientation"] = np.array(
            ScfXcfOrientation.split()[:3], dtype=float
        )

    XCF_Rotation = fdf.get("XCF_Rotation")
    if XCF_Rotation is not None:
        rotations = []
        # iterate over rows
        for rot in XCF_Rotation:
            # convert row to dictionary
            dat = np.array(rot.split()[:9], dtype=float)
            o = dat[:3]
            vw = dat[3:].reshape(2, 3)
            rotations.append(dict(o=o, vw=vw))
        fdf_arguments["ref_xcf_orientations"] = rotations

    Kset = fdf.get("INTEGRAL.Kset")
    if Kset is not None:
        fdf_arguments["kset"] = int(Kset)

    Kdirs = fdf.get("INTEGRAL.Kdirs")
    if Kdirs is not None:
        fdf_arguments["kdirs"] = Kdirs

    # This is permitted because it means automatic Ebot definition
    ebot = fdf.get("INTEGRAL.Ebot")
    try:
        fdf_arguments["ebot"] = float(ebot)
    except:
        fdf_arguments["ebot"] = None

    Eset = fdf.get("INTEGRAL.Eset")
    if Eset is not None:
        fdf_arguments["eset"] = int(Eset)

    Esetp = fdf.get("INTEGRAL.Esetp")
    if Esetp is not None:
        fdf_arguments["esetp"] = float(Esetp)

    ParallelSolver = fdf.get("GREEN.ParallelSolver")
    if ParallelSolver is not None:
        fdf_arguments["parallel_solver_for_Gk"] = bool(ParallelSolver)

    PadawanMode = fdf.get("PadawanMode")
    if PadawanMode is not None:
        fdf_arguments["padawan_mode"] = bool(PadawanMode)

    Pairs = fdf.get("Pairs")
    if Pairs is not None:
        pairs = []
        # iterate over rows
        for fdf_pair in Pairs:
            # convert data
            dat = np.array(fdf_pair.split()[:5], dtype=int)
            # create pair dictionary
            my_pair = dict(ai=dat[0], aj=dat[1], Ruc=np.array(dat[2:]))
            pairs.append(my_pair)

    MagneticEntities = fdf.get("MagneticEntities")
    if MagneticEntities is not None:
        magnetic_entities = []
        # iterate over magnetic entities
        for mag_ent in MagneticEntities:
            # drop comments from data
            row = mag_ent.split()
            dat = []
            for string in row:
                if string.find("#") != -1:
                    break
                dat.append(string)
            # cluster input
            if dat[0] in {"Cluster", "cluster"}:
                magnetic_entities.append(dict(atom=[int(_) for _ in dat[1:]]))
                continue
            # atom input, same as cluster, but raises
            # error when multiple atoms are given
            if dat[0] in {"Atom", "atom"}:
                if len(dat) > 2:
                    raise Exception("Atom input must be a single integer")
                magnetic_entities.append(dict(atom=int(dat[1])))
                continue
            # atom and shell information
            elif dat[0] in {"AtomShell", "Atomshell", "atomShell", "atomshell"}:
                magnetic_entities.append(
                    dict(atom=int(dat[1]), l=[int(_) for _ in dat[2:]])
                )
                continue
            # atom and orbital information
            elif dat[0] in {"AtomOrbital", "Atomorbital", "tomOrbital", "atomorbital"}:
                magnetic_entities.append(
                    dict(atom=int(dat[1]), orb=[int(_) for _ in dat[2:]])
                )
                continue
            # orbital information
            elif dat[0] in {"Orbitals", "orbitals"}:
                magnetic_entities.append(dict(orb=[int(_) for _ in dat[1:]]))
                continue
            else:
                raise Exception("Unrecognizable magnetic entity in .fdf!")

    return fdf_arguments, magnetic_entities, pairs


def read_py(path: str) -> ModuleType:
    """Reading input parameters from a .py file.

    Parameters
    ----------
    path: str
        The path to the input file

    Returns
    -------
    params : ModuleType
        The input parameters
    """

    # Create the spec
    spec = importlib.util.spec_from_file_location("grogupy_command_line_input", path)

    # Create the module
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    return params


if __name__ == "__main__":
    pass
