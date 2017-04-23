import argparse
from typing import Optional

CPU_BITS = 16

PREDEFINED_LABELS = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}

COMP_MAP = {
    '0': ('0', '101010'),
    '1': ('0', '111111'),
    '-1': ('0', '111010'),
    'D': ('0', '001100'),
    'A': ('0', '110000'),
    'M': ('1', '110000'),
    '!D': ('0', '001101'),
    '!A': ('0', '110001'),
    '!M': ('1', '110001'),
    '-D': ('0', '001111'),
    '-A': ('0', '110011'),
    '-M': ('1', '110011'),
    'D+1': ('0', '011111'),
    'A+1': ('0', '110111'),
    'M+1': ('1', '110111'),
    'D-1': ('0', '001110'),
    'A-1': ('0', '110010'),
    'M-1': ('1', '110010'),
    'D+A': ('0', '000010'),
    'D+M': ('1', '000010'),
    'D-A': ('0', '010011'),
    'D-M': ('1', '010011'),
    'A-D': ('0', '000111'),
    'M-D': ('1', '000111'),
    'D&A': ('0', '000000'),
    'D&M': ('1', '000000'),
    'D|A': ('0', '010101'),
    'D|M': ('1', '010101')
}

JUMP_MAP = {
    None: '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


class Instruction:
    TYPE_A = 0
    TYPE_C = 1
    TYPE_L = 2

    def __init__(self, line, instruction_type, label_name=None, address=None,
                 comp=None, jump=None):
        self._line = line
        self._type = instruction_type
        self._label_name = label_name
        self._address = address
        self._comp = comp
        self._jump = jump

    @property
    def type(self):
        return self._type

    @property
    def label_name(self):
        return self._label_name

    @property
    def label_name(self):
        return self._label_name

    @property
    def address(self):
        return self._address

    @property
    def comp(self):
        return self._comp

    @property
    def jump(self):
        return self._jump

    @staticmethod
    def from_line(line: str):
        if line.startswith('('):
            res = Instruction._parse_l_instruction(line)
        elif line.startswith('@'):
            res = Instruction.parse_a_instruction(line)
        else:
            comp, jump = Instruction._split_assign_jump(line)
            res = Instruction(line, Instruction.TYPE_C, comp=comp, jump=jump)
        return res

    @staticmethod
    def _split_assign_jump(line: str):
        if ';' not in line:
            return line, None

        assign, jump = line.split(';')
        return assign, jump

    @staticmethod
    def parse_a_instruction(line: str):
        label = line[1:]
        res = Instruction(line, Instruction.TYPE_A, address=label)
        return res

    @staticmethod
    def _parse_l_instruction(line: str):
        if not line.endswith(')'):
            raise ValueError('error when parsing', line)
        label_name = line[1:-1]
        res = Instruction(line, Instruction.TYPE_L, label_name=label_name)
        return res

    def __str__(self):
        return self._line


def is_number(text: str) -> bool:
    try:
        float(text)
        return True
    except (TypeError, ValueError):
        return False


def translate_a(instruction: Instruction, label_map: dict, labels_size: int) -> str:
    address = instruction.address

    if address in PREDEFINED_LABELS:
        address = PREDEFINED_LABELS[address]

    if is_number(address):
        address = int(address)
        res = num_to_bin_str(address)
    else:
        if address not in label_map:
            variable_place = len(label_map) - labels_size + 16
            label_map[address] = variable_place

        val = label_map[address]
        res = num_to_bin_str(val)
    return res + '\n'


def num_to_bin_str(address: int) -> str:
    res = bin(address)[2:]
    res = res.rjust(CPU_BITS, '0')
    return res


def get_d_bits(comp: str):
    res = [False, False, False]
    if '=' in comp:
        left, _ = comp.split('=')
        res[0] = 'A' in left
        res[1] = 'D' in left
        res[2] = 'M' in left
    bits = ['1' if x else '0' for x in res]
    return ''.join(bits)


def translate_c(instruction: Instruction) -> str:
    d_bits = get_d_bits(instruction.comp)
    jump_bits = JUMP_MAP[instruction.jump]

    expression = instruction.comp if '=' not in instruction.comp else instruction.comp.split('=')[1]
    a, c_bits = COMP_MAP[expression]
    res = '111' + a + c_bits + d_bits + jump_bits
    return res + '\n'


def translate(instruction: Instruction, label_map: dict, labels_size: int) -> Optional[str]:
    if instruction.type == Instruction.TYPE_A:
        return translate_a(instruction, label_map, labels_size)
    elif instruction.type == Instruction.TYPE_C:
        return translate_c(instruction)
    elif instruction.type == Instruction.TYPE_L:
        return ''
    raise TypeError('wrong instruction type')


def get_instructions(inp) -> dict:
    for line in inp:
        line = line.strip(' ').strip('\n').strip('\r\n')
        comment = line.find('//')
        if comment != -1:
            line = line[:comment]

        line = line.replace(' ', '').replace('\n', '').replace('\r\n', '')
        if line != '':
            instruction = Instruction.from_line(line)
            yield instruction


def assemble(input_file: str, output_file: str, label_map: dict):
    labels_size = len(label_map)
    with open(input_file, 'r') as inp:
        with open(output_file, 'w') as out:
            for instruction in get_instructions(inp):
                translation = translate(instruction, label_map, labels_size)
                out.write(translation)


def build_label_map(input_file: str) -> dict:
    res = {}
    with open(input_file, 'r') as inp:
        for index, instruction in enumerate(get_instructions(inp)):
            if instruction.type == Instruction.TYPE_L:
                label_name = instruction.label_name
                res[label_name] = index - len(res)

    return res


def read_program_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to the input file")
    parser.add_argument("output_file", help="path to the output file")
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    return input_file, output_file


def main():
    input_file, output_file = read_program_args()
    label_map = build_label_map(input_file)
    assemble(input_file, output_file, label_map)

if __name__ == '__main__':
    main()
