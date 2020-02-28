import unittest
import common


class ProgramTest(unittest.TestCase):
    def test_parse(self):
        filename = "sum.urm"
        program = common.program_from_file(filename)
        print(program)


if __name__ == '__main__':
    unittest.main()
