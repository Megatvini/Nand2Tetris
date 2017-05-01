import argparse

DECREASE_STACK_POINTER = '@R0\nM=M-1'
INCREASE_STACK_POINTER = '@R0\nM=M+1'


PUSH_NUMBER_INSTRUCTION = """@{}
D=A
@R0
A=M
M=D
""" + INCREASE_STACK_POINTER

PUSH_NUMBER_FROM_INDIRECT_MEMORY = """@{}
D=A
@{}
A=M+D
D=M
@R0
A=M
M=D
""" + INCREASE_STACK_POINTER

PUSH_NUMBER_FROM_MEMORY = """@{}
D=M
@R0
A=M
M=D
""" + INCREASE_STACK_POINTER

POP_INTO_INDIRECT_ADDRESS_INSTRUCTION = """@R0
A=M
A=A-1
D=M

@R13
M=D

@{}
D=A
@{}
A=M
A=A+D

D=A
@R14
M=D

@R13
D=M

@R14
A=M

M=D
""" + DECREASE_STACK_POINTER

POP_INTO_ADDRESS_INSTRUCTION = """@R0
A=M
A=A-1

D=M
@{}
M=D
""" + DECREASE_STACK_POINTER

BINARY_OP = """@R0
A=M
A=A-1
D=M
A=A-1
M=M{}D
""" + DECREASE_STACK_POINTER

GREATER_THAN_INSTRUCTIONS = """@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@GREATER_{}
D;JGT

(NOT_GREATER_{})
@R0
A=M
A=A-1
A=A-1
M=0

@END_{}
0;JMP

(GREATER_{})
@R0
A=M
A=A-1
A=A-1
M=-1

(END_{})
""" + DECREASE_STACK_POINTER

LESS_THAN_INSTRUCTIONS = """@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@LESS_{}
D;JLT

(NOT_LESS_{})
@R0
A=M
A=A-1
A=A-1
M=0

@END_{}
0;JMP

(LESS_{})
@R0
A=M
A=A-1
A=A-1
M=-1

(END_{})
""" + DECREASE_STACK_POINTER

EQUALS_INSTRUCTION = """@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@EQUALS_{}
D;JEQ

(NOT_EQUALS_{})
@R0
A=M
A=A-1
A=A-1
M=0

@END_{}
0;JMP

(EQUALS_{})
@R0
A=M
A=A-1
A=A-1
M=-1

(END_{})
""" + DECREASE_STACK_POINTER


MEMORY_ACCESS_COMMANDS = {
   'push', 'pop'
}

ARITHMETIC_OPERATIONS = {
    'add',
    'sub',
    'neg',
    'eq',
    'gt',
    'lt',
    'and',
    'or',
    'not'
}

MEMORY_CHUNKS = {
    'stack': 256,
    'static': 16,
    'local': 1,
    'argument': 2,
    'this': 3,
    'that': 4,
    'temp': 5
}


def read_program_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to the input file")
    args = parser.parse_args()
    input_file = args.input_file
    output_file = input_file[:input_file.rfind('.')] + '.asm'
    return input_file, output_file


class Instruction:
    def __init__(self, line, command, args):
        self.line = line
        self.command = command
        self.args = args

    @staticmethod
    def from_line(line: str):
        parts = line.split()
        return Instruction(line, parts[0], parts[1:])

    def __str__(self):
        return self.line


def get_instructions(inp):
    for line in inp:
        comment = line.find('//')
        if comment != -1:
            line = line[:comment]

        line = line.strip(' ').strip('\n').strip('\r\n')

        if line != '':
            instruction = Instruction.from_line(line)
            yield instruction


def push_number(num: int) -> str:
    return PUSH_NUMBER_INSTRUCTION.format(num)


def push_number_from_address(pointer_address, offset) -> str:
    return PUSH_NUMBER_FROM_INDIRECT_MEMORY.format(offset, pointer_address)


def pop_number_into_address(pointer_address, offset) -> str:
    return POP_INTO_INDIRECT_ADDRESS_INSTRUCTION.format(offset, pointer_address)


def translate_memory_access(instruction: Instruction) -> str:
    res = None
    command = instruction.command
    args = instruction.args
    if command == 'push':
        if args[0] == 'constant':
            num = int(args[1])
            res = push_number(num)
        else:
            if args[0] == 'pointer':
                res = PUSH_NUMBER_FROM_MEMORY.format(MEMORY_CHUNKS['this'] + int(args[1]))
            elif args[0] == 'temp':
                res = PUSH_NUMBER_FROM_MEMORY.format(MEMORY_CHUNKS['temp'] + int(args[1]))
            else:
                pointer_address = MEMORY_CHUNKS[args[0]]
                offset = int(args[1])
                res = push_number_from_address(pointer_address, offset)
    elif command == 'pop':
        if args[0] == 'pointer':
            res = POP_INTO_ADDRESS_INSTRUCTION.format(MEMORY_CHUNKS['this'] + int(args[1]))
        elif args[0] == 'temp':
            res = POP_INTO_ADDRESS_INSTRUCTION.format(MEMORY_CHUNKS['temp'] + int(args[1]))
        else:
            pointer_address = MEMORY_CHUNKS[args[0]]
            offset = int(args[1])
            res = pop_number_into_address(pointer_address, offset)
    return res

LABEL_COUNTER = 0


def translate_arithmetic_op(instruction: Instruction) -> str:
    global LABEL_COUNTER
    command = instruction.command
    res = None
    if command == 'add':
        res = BINARY_OP.format('+')
    elif command == 'sub':
        res = BINARY_OP.format('-')
    elif command == 'and':
        res = BINARY_OP.format('&')
    elif command == 'or':
        res = BINARY_OP.format('|')
    elif command == 'eq':
        res = EQUALS_INSTRUCTION.replace('{}', str(LABEL_COUNTER))
        LABEL_COUNTER += 1
    elif command == 'gt':
        res = GREATER_THAN_INSTRUCTIONS.replace('{}', str(LABEL_COUNTER))
        LABEL_COUNTER += 1
    elif command == 'lt':
        res = LESS_THAN_INSTRUCTIONS.replace('{}', str(LABEL_COUNTER))
        LABEL_COUNTER += 1
    elif command == 'not':
        res = '@R0\nA=M\nA=A-1\nM=!M'
    elif command == 'neg':
        res = '@R0\nA=M\nA=A-1\nM=-M'
    return res


def translate(instruction: Instruction):
    command = instruction.command
    if command in MEMORY_ACCESS_COMMANDS:
        res = translate_memory_access(instruction)
    elif command in ARITHMETIC_OPERATIONS:
        res = translate_arithmetic_op(instruction)
    else:
        raise Exception('error when translating')

    res = '//{}\n{}\n\n'.format(instruction.line, res)
    return res


def translate_to_vm(input_file, output_file):
    with open(input_file, 'r') as inp:
        with open(output_file, 'w') as out:
            for instruction in get_instructions(inp):
                translation = translate(instruction)
                out.write(translation)


def main():
    input_file, output_file = read_program_args()
    translate_to_vm(input_file, output_file)


if __name__ == '__main__':
    main()
