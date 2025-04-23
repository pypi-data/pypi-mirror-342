from ..load_nes import open_netcdf
import argparse
from mpi4py import MPI


def reorder_longitudes_cli():
    """
    Converts longitudes in a NetCDF file and saves the modified file.

    Returns:
        None
    """
    comm = MPI.COMM_WORLD
    if comm.Get_size() > 1:
        raise ValueError("Parallel not implemented yet. This script must be run with a single process.")

    parser = argparse.ArgumentParser(description="Reorder longitudes in a NetCDF file.")

    # Define expected arguments
    parser.add_argument("infile", help="Input NetCDF file path")
    parser.add_argument("outfile", help="Output NetCDF file path")

    # Parse arguments
    args = parser.parse_args()

    # Call your function with parsed arguments
    infile = args.infile
    outfile = args.outfile

    # open
    nc = open_netcdf(infile)
    # load
    nc.load()
    # convert longitudes from default_projections
    nc.convert_longitudes()
    # save
    nc.to_netcdf(outfile)
    return None
