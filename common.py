from instruction import *
from program import *

tokens = [',', '(', ')', 'Z', 'J', 'S', 'T', '\n', ' ']


def parse_file(filename: str) -> List:
    inp = open(filename, mode='r')

    lst = []
    for line in inp:
        lst.append(line.strip(' \t'))
    inp.close()
    return lst


def nat(x):
    """Smart constructor for naturals

    Arg
        x: any literal
    Returns:
        natural value
    Raises:
        ValueError if x cannot be converted into int
        or the result of this conversation is negative
    """
    try:
        n = int(x)
    except Exception as ex:
        raise ValueError("invalid literal for nat()")
    if n < 0:
        raise ValueError("invalid literal for nat()")
    return n


def isnat(x):  #
    """Function checks whether x is a natural number"""
    return isinstance(x, int) and (x >= 0)


def parse_line(line: str) -> Instruction:
    """Parser of a line into a URM-statenet

    Args:
        line: string for parsing
    Returns
        URM-statement
    """
    aux1, _, aux2 = line.partition('(')
    code = aux1.strip()
    aux1, _, _ = aux2.partition(')')
    try:
        aux2 = list(map(nat, aux1.split(',')))
    except:
        raise ValueError(
            "invalid statement format: '{}'".format(line))

    if code is None:
        code = 10

    return Instruction(code, aux2)


def program_from_file(filename: str) -> Program:
    lines = parse_file(filename)
    p = Program(lines)
    return p
