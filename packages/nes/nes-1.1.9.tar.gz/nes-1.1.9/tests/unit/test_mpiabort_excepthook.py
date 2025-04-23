import unittest
import subprocess
import sys


class TestScriptErrors(unittest.TestCase):
    @staticmethod
    def run_code_in_subprocess(code):
        # Run the code in a subprocess
        result = subprocess.run([sys.executable, '-c', code],
                                capture_output=True, text=True)
        return result

    @staticmethod
    def run_parallel_code_in_subprocess(code, num_procs=4):
        result = subprocess.run(
            ['mpirun', '-n', str(num_procs), sys.executable, '-c', code],
            capture_output=True,
            text=True
        )
        return result

    def test_raise_error_function(self):
        code = "raise ValueError('Something went wrong.')"
        result = self.run_code_in_subprocess(code)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError: Something went wrong.", result.stderr)

    def test_sys_exit_1(self):
        result = self.run_code_in_subprocess("import sys; sys.exit(1)")
        self.assertNotEqual(result.returncode, 0)

    def test_sys_exit_0(self):
        result = self.run_code_in_subprocess("import sys; sys.exit(0)")
        self.assertEqual(result.returncode, 0)

    def test_mpi_abort_0(self):
        result = self.run_code_in_subprocess("from MPI import MPI ; MPI.COMM_WORLD.Abort(0)")
        self.assertNotEqual(result.returncode, 0)

    def test_mpi_abort_1(self):
        result = self.run_code_in_subprocess("from MPI import MPI ; MPI.COMM_WORLD.Abort(1)")
        self.assertNotEqual(result.returncode, 0)

    def test_mpi_one_failure(self):
        test_code = ("def my_function():\n"
                     "    from mpi4py import MPI\n"
                     "    rank = MPI.COMM_WORLD.Get_rank()\n"
                     "    if rank == 0:\n"
                     "        raise ValueError('Something went wrong!')\n"
                     "    else:\n"
                     "        MPI.COMM_WORLD.Barrier()\n"
                     "\n"
                     "try:\n"
                     "    my_function()\n"
                     "except Exception as e:\n"
                     "    import sys\n"
                     "    from mpi4py import MPI\n"
                     "    sys.stderr.write(str(e) + '\\n')\n"
                     "    sys.stdout.write(str(e) + '\\n')\n"
                     "    MPI.COMM_WORLD.Abort(1)\n")

        result = self.run_parallel_code_in_subprocess(test_code, num_procs=1)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Something went wrong!", result.stderr)


if __name__ == '__main__':
    unittest.main()
