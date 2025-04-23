import unittest


class TestImports(unittest.TestCase):
    def test_imports(self):
        imports_to_test = [
            'sys', 'os', 'time', 'timeit', 'math', 'calendar', 'datetime',
            'warnings', 'geopandas', 'pandas', 'numpy', 'shapely',
            'mpi4py', 'netCDF4', 'pyproj', 'configargparse', 'filelock',
            'pytz',  'eccodes']

        for module_name in imports_to_test:
            with self.subTest(module=module_name):
                try:
                    __import__(module_name)
                except ImportError as e:
                    self.fail(f"Failed to import {module_name}: {e}")

    def test_eccodes(self):
        try:
            import eccodes
            from eccodes import codes_grib_new_from_file
            from eccodes import codes_keys_iterator_new
            from eccodes import codes_keys_iterator_next
            from eccodes import codes_keys_iterator_get_name
            from eccodes import codes_get_string
            from eccodes import codes_keys_iterator_delete
            from eccodes import codes_clone
            from eccodes import codes_set
            from eccodes import codes_set_values
            from eccodes import codes_write
            from eccodes import codes_release
            from eccodes import codes_samples_path
            import os
            os.path.join(codes_samples_path(), 'GRIB2.tmpl')

            print("Eccodes: ", eccodes.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_geopandas(self):
        try:
            import geopandas
            print("GeoPandas: ", geopandas.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_pandas(self):
        try:
            import pandas
            print("Pandas: ", pandas.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_numpy(self):
        try:
            import numpy
            print("NumPy: ", numpy.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_shapely(self):
        try:
            import shapely
            print("Shapely: ", shapely.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_mpi(self):
        try:
            import mpi4py
            print("mpi4py: ", mpi4py.__version__)
            from mpi4py import MPI
            print("MPI Vendor: ", MPI.get_vendor())
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_netcdf4(self):
        try:
            import netCDF4
            print("netCDF4 version:", netCDF4.__version__)
            print("HDF5 version:", netCDF4.__hdf5libversion__)
            print("NetCDF library version:", netCDF4.__netcdf4libversion__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_netcdf4_parallel(self):
        try:
            from mpi4py import MPI
            import numpy as np
            from netCDF4 import Dataset
            nc = Dataset('/tmp/parallel_test.nc', 'w', parallel=True, comm=MPI.COMM_WORLD, info=MPI.Info())
            nc.close()
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_pyproj(self):
        try:
            import pyproj
            print("pyproj: ", pyproj.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")

    def test_pytz(self):
        try:
            import pytz
            print("pytz: ", pytz.__version__)
        except ImportError as e:
            self.fail(f"Import error: {e}")


if __name__ == '__main__':
    unittest.main()
