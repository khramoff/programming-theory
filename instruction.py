import common
from typing import List


class Instruction:

    def __init__(self, instruction: str, args: List) -> None:
        self.instruction = ''
        self.arguments = []
        if instruction == 'T':
            self.transpose(args)
        elif instruction == 'J':
            self.jump(args)
        elif instruction == 'S':
            self.addition(args)
        elif instruction == 'Z':
            self.empty(args)
        else:
            raise ValueError("invalid instruction")

    def exit_point(self) -> bool:
        return self.instruction == "J" and self.arguments[-1] == 0

    def set_exit_point(self, n: int):
        if not self.exit_point():
            return
        self.arguments[-1] = n

    @staticmethod
    def check_args(args: List):
        for a in args:
            if not common.isnat(a):
                raise ValueError("arguments must be natural numbers")

        return None

    def transpose(self, args: List):
        if len(args) != 2:
            raise ValueError("transposition requires 2 arguments")

        try:
            self.check_args(args)
        except Exception as ex:
            raise ValueError("invalid literal for nat()")

        self.instruction = 'T'
        self.arguments = args

    def jump(self, args: List):
        if len(args) != 3:
            raise ValueError("jump requires 3 arguments")

        try:
            self.check_args(args)
        except Exception as ex:
            raise ValueError("invalid literal for nat()")

        self.instruction = 'J'
        self.arguments = args

    def addition(self, args: List):
        if len(args) != 1:
            raise ValueError("addition requires 1 arguments")

        try:
            self.check_args(args)
        except Exception as ex:
            raise ValueError("invalid literal for nat()")

        self.instruction = 'S'
        self.arguments = args

    def empty(self, args: List):
        if len(args) != 1:
            raise ValueError("emptying requires 1 arguments")

        try:
            self.check_args(args)
        except Exception as ex:
            raise ValueError("invalid literal for nat()")

        self.instruction = 'Z'
        self.arguments = args

    def pretty_args(self):
        text = "("
        for a in self.arguments:
            text += str(a) + ", "

        text = text[:-2]
        text += ")\n"
        return text

    def to_command(self):
        return self.instruction + self.pretty_args()

    def offset_registers(self, n: int):
        new_args = []
        args = self.arguments
        ic = []
        if self.instruction == 'J':
            args = self.arguments[:-1]
            ic = [self.arguments[-1]]

        for a in args:
            new_args.append(a + n)

        new_args.extend(ic)

        self.arguments = new_args

    def registers(self) -> List[int]:
        if self.instruction == "J":
            return self.arguments[:-1]
        else:
            return self.arguments

    def offset_command(self, n: int):
        if self.instruction != 'J':
            return
        if self.arguments[-1] == 0:
            return
        self.arguments[-1] += n
