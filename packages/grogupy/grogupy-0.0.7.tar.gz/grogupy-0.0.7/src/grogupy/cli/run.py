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
import argparse
import datetime
import os
from os.path import join
from timeit import default_timer as timer

import numpy as np

from .. import __citation__, __definitely_not_grogu__
from ..config import CONFIG
from ..io.io import load, read_py, save, save_magnopy, save_UppASD
from ..physics import Builder, Contour, Hamiltonian, Kspace

PRINTING = False
if CONFIG.is_CPU:
    from mpi4py import MPI

    rank = MPI.COMM_WORLD.rank
    if rank == 0:
        PRINTING = True
elif CONFIG.is_GPU:
    PRINTING = True
else:
    raise Exception


def main():
    """Main entry point of the script."""
    if PRINTING:
        print("Simulation started at:", datetime.datetime.now())
    start = timer()

    # setup parser
    parser = argparse.ArgumentParser(
        description="Load Python variables from a .py file."
    )
    parser.add_argument(
        "file", nargs="?", help="Path to a Python file containing variables to load."
    )
    parser.add_argument(
        "--cite",
        dest="cite",
        action="store_true",
        default=False,
        help="Print the citation of the package.",
    )
    # parameters from command line
    args = parser.parse_args()

    # print citation if needed
    if args.cite:
        print(__citation__ + __definitely_not_grogu__)
        if args.file is None:
            return

    # Reading input
    params = read_py(args.file)

    # only citation
    if params is None:
        return

    # construct the input and output file paths
    infile = join(params.infolder, params.infile)
    if not infile.endswith(".fdf"):
        infile += ".fdf"
    outfile = join(params.outfolder, params.outfile)

    # Define simulation
    simulation = Builder(
        ref_xcf_orientations=params.ref_xcf_orientations, matlabmode=params.matlabmode
    )

    # Add solvers and parallellizations
    simulation.greens_function_solver = params.greens_function_solver
    simulation.exchange_solver = params.exchange_solver
    simulation.anisotropy_solver = params.anisotropy_solver
    simulation.low_memory_mode = params.low_memory_mode
    # Define Kspace
    kspace = Kspace(
        kset=params.kset,
    )

    # Define Contour
    contour = Contour(
        eset=params.eset,
        esetp=params.esetp,
        emin=params.emin,
        emax=params.emax,
        emin_shift=params.emin_shift,
        emax_shift=params.emax_shift,
        eigfile=infile,
    )

    # Define Hamiltonian from sisl
    hamiltonian = Hamiltonian(
        infile=infile,
        scf_xcf_orientation=params.scf_xcf_orientation,
    )

    # Add instances to the simulation
    simulation.add_kspace(kspace)
    simulation.add_contour(contour)
    simulation.add_hamiltonian(hamiltonian)

    # Set up magnetic entities and pairs
    # If it is not set up from range:
    if not params.setup_from_range:
        simulation.add_magnetic_entities(params.magnetic_entities)
        simulation.add_pairs(params.pairs)

    # If it is automatically set up from range
    if params.setup_from_range:
        if not isinstance(params.atomic_subset, list):
            params.atomic_subset = [params.atomic_subset]

        tags = []
        for at in hamiltonian._dh.atoms:
            tags.append(at.tag)
        tags = np.array(tags)

        atoms = []
        for i, tag in enumerate(tags):
            if tag in params.atomic_subset:
                atoms.append(i)

        simulation.setup_from_range(
            params.radius, [atoms, atoms], **params.kwargs_for_mag_ent
        )

    if PRINTING:
        print("setup:", (timer() - start) / 60, " min")
        print("\n\n\n")
        print(
            "################################################################################"
        )
        print(
            "################################################################################"
        )
        print(simulation)
        print(
            "################################################################################"
        )
        print(
            "################################################################################"
        )
        print("\n\n\n")

    if params.max_pairs_per_loop < len(simulation.pairs):
        number_of_chunks = (
            np.floor(len(simulation.pairs) / params.max_pairs_per_loop) + 1
        )
        pair_chunks = np.array_split(simulation.pairs, number_of_chunks)

        if PRINTING:
            print("\n\n\n")
            print(
                "################################################################################"
            )
            print(
                "################################################################################"
            )
            print(
                "Maximum number of pairs per loop exceeded! To avoid memory overflow pairs are being separated."
            )
            print(f"Maximum number of pairs per loop {params.max_pairs_per_loop}")
            print(
                f"pairs are being separated to {number_of_chunks} chunks, each chunk containing {[len(c) for c in pair_chunks]} pairs."
            )
            print("These will be ran as separate and they will be concatenated.")
            print(
                "################################################################################"
            )
            print(
                "################################################################################"
            )
            print("\n\n\n")

        # run chunks
        for i, chunk in enumerate(pair_chunks):
            simulation.pairs = chunk
            simulation.solve()
            save(
                object=simulation,
                path=join(params.outfolder, "grogupy_temp_" + str(i)),
                compress=params.pickle_compress_level,
            )
        new_pairs = []
        for i in range(len(pair_chunks)):
            new_pairs += load("./grogupy_temp_" + str(i) + ".pkl").pairs
        simulation.pairs = new_pairs

    else:
        # Solve
        simulation.solve()

    if PRINTING:
        print("\n\n\n")
        print(
            "################################################################################"
        )
        print(
            "################################################################################"
        )
        print("solved:", (timer() - start) / 60, "min")
        print(simulation.times.times)
        print(
            simulation.to_magnopy(
                precision=params.magnopy_precision, comments=params.magnopy_comments
            )
        )
        print(
            "################################################################################"
        )
        print(
            "################################################################################"
        )
        print("\n\n\n")

        if params.save_magnopy:
            save_magnopy(
                simulation,
                path=outfile,
                magnetic_moment=params.out_magentic_moment,
                precision=params.magnopy_precision,
                comments=params.magnopy_comments,
            )
            print("Saved magnopy")

        if params.save_UppASD:
            save_UppASD(
                simulation,
                folder=params.outfolder,
                magnetic_moment=params.out_magentic_moment,
            )
            print("Saved UppASD")

        if params.save_pickle:
            save(object=simulation, path=outfile, compress=params.pickle_compress_level)
            print("Saved pickle")

    if PRINTING:
        if params.max_pairs_per_loop < len(simulation.pairs):
            for i in range(len(pair_chunks)):
                os.remove("./grogupy_temp_" + str(i) + ".pkl")

        print("\n\n\n")
        print(__definitely_not_grogu__)
        print("Simulation ended at:", datetime.datetime.now())
        print("GROGUPY_NORMAL_EXIT")


if __name__ == "__main__":
    main()
