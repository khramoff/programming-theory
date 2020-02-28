from common import *
import sys, getopt


def superposition(input: str, output: str):
    inp = open(input, mode='r')
    n = int(inp.readline())
    k = int(inp.readline())

    file_lst = inp.readlines()
    inp.close()
    f_function = file_lst[0].strip(" \n\t").rstrip(" \n\t")
    g_functions = file_lst[1:]

    f_program = program_from_file(f_function)
    f_program.set_arg_count(k)

    g_programs = [program_from_file(i.strip(" \n\t").rstrip(" \n\t")) for i in g_functions]
    for g in g_programs:
        g.set_arg_count(n)

    output = open(output, "w")

    command_offset = 0
    offset = n + 1
    # cell numbers with g functions results
    g_results = list()
    for g in g_programs:
        g_results.append(offset)
        g.offset_registers_with_copy(offset)
        offset += g.max_register + 1

        g.offset_commands(command_offset + len(g.offset_instructions))
        ic = g.instruction_count()
        command_offset += ic
        g.set_exit_point(command_offset + 1)
        output.writelines(g.lines())

    f_program.offset_registers_from_list(offset, g_results)
    f_program.offset_commands(command_offset + len(f_program.offset_instructions))
    ic = f_program.instruction_count()
    command_offset += ic
    f_program.set_exit_point(command_offset + 1)

    f_program.instructions.append(Instruction("T", [offset, 0]))
    output.writelines(f_program.lines())
    output.close()


def recursion(input: str, output: str):
    inp = open(input, mode='r')
    n = int(inp.readline())

    file_lst = inp.readlines()
    inp.close()
    f_function = file_lst[0].strip(" \n\t").rstrip(" \n\t")
    g_function = file_lst[1].strip(" \n\t").rstrip(" \n\t")

    f_program = program_from_file(f_function)
    f_program.set_arg_count(n)

    g_program = program_from_file(g_function)
    g_program.set_arg_count(n + 2)

    output = open(output, "w")

    offset = n + 3
    command_offset = 5

    # This set of instructions serves as an entry point for a program
    #  and allows to return result easily without memorizing
    # register/command numbers down the line.

    output.writelines(Instruction("J", [0, 0, 6]).to_command())  # 1
    output.writelines(Instruction("T", [n + 3, 0]).to_command())  # 2
    output.writelines(Instruction("J", [0, 0, 0]).to_command())  # 3

    f_program.offset_registers_from_list(offset, [i for i in range(1, f_program.arg_count + 1)])
    f_program.offset_commands(command_offset)
    ic = f_program.instruction_count()
    command_offset += ic
    f_program.set_exit_point(command_offset + 1)
    offset += f_program.max_register + 1

    offset += f_program.max_register + 1
    recur = offset
    # This is here to return result of the recursion after number of loops is sufficient
    output.writelines(Instruction("T", [recur, 0]).to_command())  # 4
    output.writelines(Instruction("J", [0, 0, 0]).to_command())  # 5

    output.writelines(f_program.lines())

    output.writelines(Instruction("T", [recur, n + 3]).to_command())  # 5 + f.instruction_count() + 1
    output.writelines(Instruction("J", [n + 1, n + 2, 2]).to_command())  # 5 + f.instruction_count() + 2
    output.writelines(Instruction("S", [n + 2]).to_command())  # --- + 3
    command_offset += 3

    # For recursion purposes copy result of F to input args of G
    # output.close()
    transpose = [i for i in range(1, g_program.arg_count+1)]
    transpose[-1] = recur
    transpose[-2] = n + 1
    g_program.offset_registers_from_list(offset, transpose)
    command_offset += len(g_program.offset_instructions)
    g_program.offset_commands(command_offset)
    g_program.set_exit_point(5 + f_program.instruction_count() + 1)
    output.writelines(g_program.lines())

    output.close()


def minimization(input: str, output: str):
    inp = open(input, mode='r')
    n = int(inp.readline())

    f = inp.readline().strip(" \n\t").rstrip(" \n\t")
    inp.close()
    f_program = program_from_file(f)
    f_program.set_arg_count(n + 1)

    output = open(output, "w")

    initial_jump = Instruction("J", [0, 0, 4])
    output.writelines(initial_jump.to_command())
    output.writelines(Instruction("T", [n + 1, 0]).to_command())
    output.writelines(Instruction("J", [0, 0, 0]).to_command())
    output.writelines(Instruction("Z", [n + 1]).to_command())

    offset = n + 2
    command_offset = 4

    f_program.offset_registers_with_copy(offset)
    f_program.offset_commands(command_offset)

    command_offset += f_program.instruction_count()
    f_program.set_exit_point(command_offset + 1)
    output.writelines(f_program.lines())

    output.writelines(Instruction("J", [0, n + 2, 2]).to_command())
    output.writelines(Instruction("S", [n + 1]).to_command())
    copy_x = [Instruction("T", [i, i + n]) for i in range(1, n + 1)]

    for i in copy_x:
        output.writelines(i.to_command())

    output.writelines(Instruction("J", [0, 0, 5]).to_command())

    output.close()


def main(argv):
    input_file = ''
    output_file = ''
    command = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:c:", ["ifile=", "ofile=", "command="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile> -c <command>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile> -c <command>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-c", "--command"):
            command = arg
    print('Input file is', input_file)
    print('Output file is', output_file)
    print('Command is', command)

    if command == "s":
        superposition(input_file, output_file)
    elif command == "r":
        recursion(input_file, output_file)
    elif command == "m":
        minimization(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
