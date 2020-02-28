import unittest
import instruction


class MyTestCase(unittest.TestCase):
    def test_something(self):
        i = "J"
        args = [1, 2, 3]
        jump_instruction = instruction.Instruction()
        jump_instruction.from_raw(i, args)
        print(jump_instruction.to_command())

if __name__ == '__main__':
    unittest.main()
