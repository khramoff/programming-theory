from instruction import *

StringList = List[str]
metaPrefix = "#meta"


class Program:
    def __init__(self, lines: StringList):
        self.instructions = list()
        # metadata
        meta = ""
        registers = set()
        for l in lines:
            if l.startswith(metaPrefix):
                meta = l[len(metaPrefix):]
                continue

            i = common.parse_line(l)
            self.instructions.append(i)
            registers.update(set(i.registers()))
        self.max_register = max(registers)
        if meta != "":
            self.arg_count = common.nat(meta)
        else:
            self.arg_count = 0

        self.offset_instructions = []
        self.register_offset = 0
        self.instruction_offset = 0

    def set_arg_count(self, n: int):
        self.arg_count = n

    def get_arg_count(self) -> int:
        return self.arg_count

    def instruction_count(self) -> int:
        return len(self.instructions) + len(self.offset_instructions)

    def lines(self) -> StringList:
        l = list()
        for o in self.offset_instructions:
            l.append(o.to_command())

        for i in self.instructions:
            l.append(i.to_command())
        return l

    def __repr__(self):
        lines = self.lines()
        s = ""
        for l in lines:
            s += l
        return s

    def offset_registers_with_copy(self, n: int):
        self.register_offset = n
        self.offset_instructions = [Instruction("T", [i, i + n]) for i in range(1, self.arg_count + 1)]
        for i in self.instructions:
            i.offset_registers(n)

    def offset_registers_from_list(self, n: int, reg_from: List):
        new = [i+n for i in range(1, self.arg_count + 1)]
        transpose_args = list(zip(reg_from, new))
        self.register_offset = n
        self.offset_instructions = [Instruction("T", list(i)) for i in transpose_args]
        for i in self.instructions:
            i.offset_registers(n)

    def offset_commands(self, n: int):
        self.instruction_offset = n
        for i in self.instructions:
            i.offset_command(n)

    def set_exit_point(self, n: int):
        for i in self.instructions:
            if i.exit_point():
                i.set_exit_point(n)

        # if no_exit_point:
        #     self.instructions.append(Instruction("J", [0, 0, n]))
