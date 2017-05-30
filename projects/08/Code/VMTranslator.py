import argparse
import os

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
    'local': 1,
    'argument': 2,
    'this': 3,
    'that': 4,
    'temp': 5
}


def is_file(path: str) -> bool:
    res = os.path.isfile(path)
    return res


def get_file_list(folder_dir: str) -> list:
    if not folder_dir.endswith('/'):
        folder_dir += '/'
    sub_files = [folder_dir + x for x in os.listdir(folder_dir)]
    res = [x for x in sub_files if is_file(x)]
    return res


def get_input_file_paths(input_path: str) -> list:
    if is_file(input_path):
        return [input_path]
    else:
        return get_file_list(input_path)


def read_program_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="path to the input file or directory")
    args = parser.parse_args()
    input_paths = [x for x in get_input_file_paths(args.input_path) if x.endswith('.vm')]
    output_file = get_output_file_path(args.input_path)
    return input_paths, output_file


def get_output_file_path(input_path):
    if is_file(input_path):
        output_file = input_path[:input_path.rfind('.')] + '.asm'
    else:
        output_file = (input_path + '/' + get_dir_name(input_path) + '.asm').replace('//', '/')
    return output_file


def get_dir_name(path: str) -> str:
    spl = path.split('/')
    if path.endswith('/'):
        return spl[-2]
    else:
        return spl[-1]


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

        line = line.strip('\n').strip('\r\n').strip(' ')

        if line != '':
            instruction = Instruction.from_line(line)
            yield instruction


def push_number(num: int) -> str:
    return PUSH_NUMBER_INSTRUCTION.format(num)


def push_number_from_address(pointer_address, offset) -> str:
    return PUSH_NUMBER_FROM_INDIRECT_MEMORY.format(offset, pointer_address)


def pop_number_into_address(pointer_address, offset) -> str:
    return POP_INTO_INDIRECT_ADDRESS_INSTRUCTION.format(offset, pointer_address)


def translate_memory_access(instruction: Instruction, class_name: str) -> str:
    res = None
    command = instruction.command
    args = instruction.args
    if command == 'push':
        if args[0] == 'constant':
            num = int(args[1])
            res = push_number(num)
        elif args[0] == 'pointer':
            res = PUSH_NUMBER_FROM_MEMORY.format(MEMORY_CHUNKS['this'] + int(args[1]))
        elif args[0] == 'temp':
            res = PUSH_NUMBER_FROM_MEMORY.format(MEMORY_CHUNKS['temp'] + int(args[1]))
        elif args[0] == 'static':
            res = PUSH_NUMBER_FROM_MEMORY.format('{}.{}'.format(class_name, args[1]))
        else:
            pointer_address = MEMORY_CHUNKS[args[0]]
            offset = int(args[1])
            res = push_number_from_address(pointer_address, offset)
    elif command == 'pop':
        if args[0] == 'pointer':
            res = POP_INTO_ADDRESS_INSTRUCTION.format(MEMORY_CHUNKS['this'] + int(args[1]))
        elif args[0] == 'temp':
            res = POP_INTO_ADDRESS_INSTRUCTION.format(MEMORY_CHUNKS['temp'] + int(args[1]))
        elif args[0] == 'static':
            res = POP_INTO_ADDRESS_INSTRUCTION.format('{}.{}'.format(class_name, args[1]))
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


def translate_label(instruction: Instruction) -> str:
    res = '({})\n'.format(instruction.args[0])
    return res


def translate_if_go_to(instruction: Instruction) -> str:
    res = ('@SP\nA=M-1\nD=M\n' + DECREASE_STACK_POINTER + '\n@{}\nD;JNE\n').format(instruction.args[0])
    return res


def translate_go_to(instruction: Instruction) -> str:
    res = '@{}\n0;JMP\n'.format(instruction.args[0])
    return res


def translate_function(instruction: Instruction) -> str:
    res = translate(Instruction.from_line('label {}'.format(instruction.args[0])))
    for _ in range(int(instruction.args[1])):
        res += translate(Instruction.from_line('push constant 0'))
    return res


def translate_call(instruction: Instruction) -> str:
    # push return address
    global LABEL_COUNTER
    label = 'return_{}_{}'.format(instruction.args[0], LABEL_COUNTER)
    res = '@{}\n'.format(label)
    res += 'D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

    # push lcl
    res += PUSH_NUMBER_FROM_MEMORY.format('LCL') + '\n'
    # push arg
    res += PUSH_NUMBER_FROM_MEMORY.format('ARG') + '\n'
    # push this
    res += PUSH_NUMBER_FROM_MEMORY.format('THIS') + '\n'
    # push that
    res += PUSH_NUMBER_FROM_MEMORY.format('THAT') + '\n'

    # arg = SP-nArgs-5
    res += '@SP\nD=M\n@{}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n'.format(instruction.args[1])
    # lcl = SP
    res += '@SP\nD=M\n@LCL\nM=D\n'
    # goto func
    res += '@{}\n0;JMP\n'.format(instruction.args[0])

    res += '({})'.format(label)
    LABEL_COUNTER += 1
    return res

RETURN_ASM = """//retAddr = *(LCL - 5)
@LCL
D=M
@5
A=D-A
D=M
@retAddr
M=D

//*ARG = pop
@SP
A=M-1
D=M
@ARG
A=M
M=D

//SP = ARG + 1
@ARG
D=M+1
@SP
M=D

//THAT = *(LCL-1)
@LCL
A=M-1
D=M
@THAT
M=D

//THIS = *(LCL-2)
@2
D=A
@LCL
A=M-D
D=M
@THIS
M=D

//ARG = *(LCL-3)
@3
D=A
@LCL
A=M-D
D=M
@ARG
M=D

//LCL = *(LCL-4)
@4
D=A
@LCL
A=M-D
D=M
@LCL
M=D

//goto retAddr
@retAddr
A=M
0;JMP

"""


def translate_return() -> str:
    return RETURN_ASM


def translate(instruction: Instruction, class_name: str='NO_CLASS'):
    command = instruction.command
    if command in MEMORY_ACCESS_COMMANDS:
        res = translate_memory_access(instruction, class_name)
    elif command in ARITHMETIC_OPERATIONS:
        res = translate_arithmetic_op(instruction)
    elif command == 'label':
        res = translate_label(instruction)
    elif command == 'goto':
        res = translate_go_to(instruction)
    elif command == 'if-goto':
        res = translate_if_go_to(instruction)
    elif command == 'function':
        res = translate_function(instruction)
    elif command == 'call':
        res = translate_call(instruction)
    elif command == 'return':
        res = translate_return()
    else:
        raise Exception('error when translating')

    res = '//{}\n{}\n\n'.format(instruction.line, res)
    return res


def has_sys_vm(input_files: list) -> bool:
    res = any([x.endswith('Sys.vm') for x in input_files])
    return res

BOOTSTRAP_CODE = """@256
D=A
@SP
M=D

""" + translate(Instruction.from_line('call Sys.init 0'))


def get_class_name(input_file: str) -> str:
    res = input_file.split('/')[-1].split('.')[0]
    return res


def translate_to_vm(input_files: list, output_file: str):
    with open(output_file, 'w') as out:
        if has_sys_vm(input_files):
            out.write(BOOTSTRAP_CODE)
        for input_file in input_files:
            class_name = get_class_name(input_file)
            with open(input_file, 'r') as inp:
                for instruction in get_instructions(inp):
                    translation = translate(instruction, class_name)
                    out.write(translation)


def main():
    input_files, output_file = read_program_args()
    translate_to_vm(input_files, output_file)


if __name__ == '__main__':
    main()
