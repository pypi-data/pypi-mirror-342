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

from .. import __citation__, __definitely_not_grogu__
from ..io.io import load, save_magnopy
from ..viz.viz import (
    plot_contour,
    plot_DMI,
    plot_kspace,
    plot_magnetic_entities,
    plot_pairs,
)


def main():
    """Main entry point of the script."""

    # setup parser
    parser = argparse.ArgumentParser(description="Load results from a .pkl file.")
    parser.add_argument(
        "file", nargs="?", help="Path to a .pkl file containing the results."
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
    system = load(args.file)
    # get the output name
    name = args.file
    if name.endswith(".pkl"):
        name = name[:-4]

    print(f"The output files are under the name: {name}")
    print(__definitely_not_grogu__)

    with open(name + ".analysis.txt", "w") as f:
        f.writelines(system.to_magnopy())

    fig = plot_contour(system.contour)
    fig.write_html(name + ".contour.html")

    fig = plot_kspace(system.kspace)
    fig.write_html(name + ".kspace.html")

    fig = plot_magnetic_entities(system)
    fig.write_html(name + ".magnetic_entities.html")

    fig = plot_pairs(system)
    fig.write_html(name + ".pairs.html")

    fig = plot_DMI(system).add_traces(system.plot_pairs(connect=True).data)
    fig.write_html(name + ".DMIs.html")


if __name__ == "__main__":
    main()
