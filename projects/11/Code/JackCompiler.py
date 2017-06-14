import argparse
import os

THAT = 'that'

ELSE = 'else'

TEMP = 'temp'

OPERATIONS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

IF_LABEL_COUNTER = 0

WHILE_LABEL_COUNTER = 0

VM_OP_MAP = {
    '+': 'add',
    '-': 'sub',
    '*': 'Math.multiply',
    '/': 'Math.divide',
    '&': 'and',
    '|': 'or',
    '<': 'lt',
    '>': 'gt',
    '=': 'eq',
    '~': 'not'
}

NULL = 'null'

FALSE = 'false'

TRUE = 'true'

THIS = 'this'

LOCAL = 'local'

STATIC = 'static'

POINTER = 'pointer'

CONSTRUCTOR = 'constructor'

FIELD = 'field'

ARGUMENT = 'argument'

METHOD = 'method'

CONSTANT = 'constant'

TOKENS = 'tokens'

EXPRESSION = 'expression'

LET_STATEMENT = 'letStatement'

IF_STATEMENT = 'ifStatement'

WHILE_STATEMENT = 'whileStatement'

KEYWORD_CONSTANTS = ['true', 'false', 'null', 'this']

TERM = 'term'

EXPRESSION_LIST = 'expressionList'

DO_STATEMENT = 'doStatement'

RETURN_STATEMENT = 'returnStatement'

VAR = 'var'

RETURN = 'return'

DO = 'do'

WHILE = 'while'

IF = 'if'

LET = 'let'

VAR_DEC = 'varDec'

STATEMENTS = 'statements'

PARAMETER_LIST = 'parameterList'

SUBROUTINE_BODY = 'subroutineBody'

CLASS_VAR_TYPES = ['field', 'static']

CLASS_VAR_DEC = 'classVarDec'

SUBROUTINE_NAMES = ['method', 'function', 'constructor']

SUBROUTINE_DEC = 'subroutineDec'

CLASS = 'class'

KEYWORD = 'keyword'
SYMBOL = 'symbol'
INTEGER_CONSTANT = 'integerConstant'
STRING_CONSTANT = 'stringConstant'
IDENTIFIER = 'identifier'


KEYWORDS = {
    'class', 'constructor', 'function',
    'method', 'field', 'static', 'var',
    'int', 'char', 'boolean', 'void',
    'true', 'false', 'null',  'this',
    'let', 'do', 'if', 'else', 'while',
    'return'
}

SYMBOLS = {
    '(', ')', '{', '}', '[', ']', '.', ',', ';', '+',
    '-', '*', '/', '&', '|', '<', '>', '=', '~'
}

CUR_CLASS_NAME = 'Main'


class VMWriter:
    def __init__(self, output_file: str):
        self._out_file = open(output_file, 'w')

    def write_push(self, segment: str, index: int):
        if segment == CONSTANT and index < 0:
            self.write_push(CONSTANT, -index)
            self.write('neg')
        self._out_file.write('push {} {}\n'.format(segment, index))

    def write_pop(self, segment: str, index: int):
        self._out_file.write('pop {} {}\n'.format(segment, index))

    def write_label(self, label: str):
        self._out_file.write('label {}\n'.format(label))

    def write_go_to(self, label: str):
        self._out_file.write('goto {}\n'.format(label))

    def write_if(self, label: str):
        self._out_file.write('if-goto {}\n'.format(label))

    def write_call(self, function_name: str, num_args: int):
        self._out_file.write('call {} {}\n'.format(function_name, num_args))

    def write_function(self, function_name: str, n_local_vars: int):
        self._out_file.write('function {} {}\n'.format(function_name, n_local_vars))

    def write_return(self):
        self._out_file.write('return\n')

    def write_comment(self, text: str):
        self._out_file.write('//' + text + '\n')

    def write_op(self, op: str, is_unary=False):
        if is_unary and op == '-':
            self._out_file.write('neg\n')
            return

        vm_op = VM_OP_MAP[op]
        if '.' in vm_op:
            self.write_call(vm_op, 2)
        else:
            self._out_file.write(vm_op + ' \n')

    def close(self):
        self._out_file.close()

    def write(self, text: str):
        self._out_file.write(text + '\n')


class Tokenizer:
    def __init__(self, input_file_path: str):
        self._input_file = input_file_path
        self._tokens = list(self._get_tokens())
        self._cur_index = 0

    def pop(self) -> tuple:
        if self.is_empty():
            raise RuntimeError()
        res = self._tokens[self._cur_index]
        self._cur_index += 1
        return res

    def peek(self) -> tuple:
        if self.is_empty():
            raise RuntimeError()
        return self._tokens[self._cur_index]

    def is_empty(self):
        return self._cur_index == len(self._tokens)

    def _get_tokens(self):
        with open(self._input_file) as inp:
            full_text = inp.read()
            full_text = remove_comments(full_text)
            return parse_full_text(full_text)

    def __str__(self):
        return self.peek()[1]


def get_input_output(input_path: str) -> tuple:
    if input_path.endswith('/'):
        input_path = input_path[:-1]

    if not os.path.exists(input_path):
        raise FileNotFoundError()

    if os.path.isfile(input_path):
        file_paths = [input_path]
        output_path = '/'.join(input_path.split('/')[:-1])
    else:
        files = os.listdir(input_path)
        file_paths = [input_path + '/' + x for x in files]
        output_path = input_path

    jack_files = [x for x in file_paths if x.endswith('.jack')]

    return jack_files, output_path


def read_program_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="path to the input file or directory")
    args = parser.parse_args()
    input_path = args.input_path
    return get_input_output(input_path)


def is_number(text: str):
    try:
        int(text)
        return True
    except ValueError as _:
        return False


def get_token_type(token: str):
    if token in KEYWORDS:
        return KEYWORD, token

    if token in SYMBOLS:
        return SYMBOL, token

    if is_number(token):
        return INTEGER_CONSTANT, token

    if token.startswith('"'):
        return STRING_CONSTANT, token.replace('"', '')

    return IDENTIFIER, token

DELIMITERS = {' ', '\n', '\r\n', '\t'}


def parse_full_text(full_text: str) -> tuple:
    buffer = ''
    reading_string = False
    for ch in full_text:
        if reading_string:
            buffer += ch
        else:
            if ch in DELIMITERS:
                if len(buffer) > 0:
                    yield get_token_type(buffer)
                    buffer = ''
            elif ch in SYMBOLS:
                if len(buffer) > 0:
                    yield get_token_type(buffer)
                    buffer = ''
                yield get_token_type(ch)
            else:
                buffer += ch

        if ch == '"':
            reading_string = not reading_string


def find_all_strings(x: str) -> list:
    indices = find_all(x, '"')
    res = []
    for i in range(0, len(indices), 2):
        res.append((indices[i], indices[i+1]))

    return res


def find_all(x: str, sub_str: str) -> list:
    indices = []
    found = x.find(sub_str)
    while found != -1:
        indices.append(found)
        found = x.find(sub_str, found + 1)
    return indices


def crosses(slash_index: int, string_literals: list) -> bool:
    for start, end in string_literals:
        if start <= slash_index <= end:
            return True
    return False


def remove_comments(full_text: str) -> str:
    lines = []

    for x in full_text.splitlines(True):
        string_literals = find_all_strings(x)
        all_slashes = find_all(x, '//')
        for slash_index in all_slashes:
            if not crosses(slash_index, string_literals):
                x = x[:slash_index]
                break
        lines.append(x)

    res = ''.join(lines)

    while '/**' in res:
        start = res.find('/**')
        end = res.find('*/', start)
        res = res[:start] + res[end + 2:]
    return res


def count_num_vars(variable_scope: str, class_symbol_table: dict) -> int:
    res = 0
    for cur_var_scope, _, _ in class_symbol_table.values():
        if cur_var_scope == variable_scope:
            res += 1
    return res


def compile_class_var_dec(tokenizer: Tokenizer, class_symbol_table: dict):

    variable_scope = tokenizer.pop()[1]  # static | field
    variable_type = tokenizer.pop()[1]  # type
    variable_name = tokenizer.pop()[1]  # variable name

    num_vars = count_num_vars(variable_scope, class_symbol_table)
    class_symbol_table[variable_name] = (variable_scope, variable_type, num_vars)

    num_vars += 1
    while tokenizer.peek()[1] == ',':
        assert tokenizer.pop() == (SYMBOL, ',')  # ,
        variable_name = tokenizer.pop()[1]  # variable name
        class_symbol_table[variable_name] = (variable_scope, variable_type, num_vars)
        num_vars += 1

    assert tokenizer.pop() == (SYMBOL, ';')  # ;


def compile_variable_dec(tokenizer: Tokenizer, subroutine_symbol_table: dict):
    assert tokenizer.pop() == (KEYWORD, VAR)  # var
    var_type = tokenizer.pop()[1]  # type
    var_name = tokenizer.pop()[1]  # varName
    num_vars = count_num_vars(VAR, subroutine_symbol_table)
    subroutine_symbol_table[var_name] = (VAR, var_type, num_vars)
    num_vars += 1
    while tokenizer.peek()[1] == ',':
        assert tokenizer.pop() == (SYMBOL, ',')  # ,
        var_name = tokenizer.pop()[1]  # varName
        subroutine_symbol_table[var_name] = (VAR, var_type, num_vars)
        num_vars += 1

    assert tokenizer.pop() == (SYMBOL, ';')  # ;


def compile_expression(tokenizer: Tokenizer,
                       writer: VMWriter,
                       class_symbol_table: dict,
                       subroutine_symbol_table: dict):
    compile_term(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    while tokenizer.peek()[1] in OPERATIONS:
        op = tokenizer.pop()[1]  # op
        compile_term(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        writer.write_op(op)


def scope_to_segment(var_scope: str) -> str:
    if var_scope == FIELD:
        return THIS
    if var_scope == VAR:
        return LOCAL

    return var_scope


def compile_let_statement(tokenizer: Tokenizer,
                          writer: VMWriter,
                          class_symbol_table: dict,
                          subroutine_symbol_table: dict):
    assert tokenizer.pop() == (KEYWORD, LET)  # let

    var_name = tokenizer.pop()[1]  # varName
    if var_name in class_symbol_table:
        var_scope, _, var_index = class_symbol_table[var_name]
    else:
        var_scope, _, var_index = subroutine_symbol_table[var_name]
    memory_segment = scope_to_segment(var_scope)

    if tokenizer.peek()[1] == '[':
        writer.write_push(memory_segment, var_index)
        assert tokenizer.pop() == (SYMBOL, '[')
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        assert tokenizer.pop() == (SYMBOL, ']')
        writer.write('add')
        writer.write_pop(TEMP, 0)

        assert tokenizer.pop() == (SYMBOL, '=')  # =
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        assert tokenizer.pop() == (SYMBOL, ';')  # ;

        writer.write_push(TEMP, 0)
        writer.write_pop(POINTER, 1)
        writer.write_pop(THAT, 0)
    else:
        assert tokenizer.pop() == (SYMBOL, '=')  # =
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        assert tokenizer.pop() == (SYMBOL, ';')  # ;
        writer.write_pop(memory_segment, var_index)


def compile_if_statement(tokenizer: Tokenizer,
                         writer: VMWriter,
                         class_symbol_table: dict,
                         subroutine_symbol_table: dict):
    global IF_LABEL_COUNTER
    label_else = 'ELSE_{}'.format(IF_LABEL_COUNTER)
    label_done = 'IF_DONE_{}'.format(IF_LABEL_COUNTER)
    IF_LABEL_COUNTER += 1

    assert tokenizer.pop() == (KEYWORD, IF)  # if
    assert tokenizer.pop() == (SYMBOL, '(')  # (
    compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    assert tokenizer.pop() == (SYMBOL, ')')  # )
    writer.write('not')
    writer.write_if(label_else)
    assert tokenizer.pop() == (SYMBOL, '{')  # {
    compile_statements(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    writer.write_go_to(label_done)
    writer.write_label(label_else)
    assert tokenizer.pop() == (SYMBOL, '}')  # }
    if tokenizer.peek()[1] == ELSE:
        assert tokenizer.pop() == (KEYWORD, ELSE)  # else
        assert tokenizer.pop() == (SYMBOL, '{')  # {
        compile_statements(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        assert tokenizer.pop() == (SYMBOL, '}')  # }
    writer.write_label(label_done)


def compile_while_statement(tokenizer: Tokenizer,
                            writer: VMWriter,
                            class_symbol_table: dict,
                            subroutine_symbol_table: dict):
    global WHILE_LABEL_COUNTER
    label_while = 'WHILE_{}'.format(WHILE_LABEL_COUNTER)
    label_done = 'WHILE_DONE_{}'.format(WHILE_LABEL_COUNTER)
    WHILE_LABEL_COUNTER += 1
    assert tokenizer.pop() == (KEYWORD, WHILE)  # while
    assert tokenizer.pop() == (SYMBOL, '(')  # (
    writer.write_label(label_while)
    compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    writer.write('not')
    writer.write_if(label_done)
    assert tokenizer.pop() == (SYMBOL, ')')  # )
    assert tokenizer.pop() == (SYMBOL, '{')  # {
    compile_statements(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    writer.write_go_to(label_while)
    writer.write_label(label_done)
    assert tokenizer.pop() == (SYMBOL, '}')  # }


def compile_term(tokenizer: Tokenizer,
                 writer: VMWriter,
                 class_symbol_table: dict,
                 subroutine_symbol_table: dict):
    token_type, token = tokenizer.pop()
    next_token_type, next_token = tokenizer.peek()
    if is_number(token):
        writer.write_push(CONSTANT, int(token))
    elif token_type == STRING_CONSTANT:
        str_len = len(token)
        writer.write_push(CONSTANT, str_len)
        writer.write_call('String.new', 1)
        for ch in token:
            writer.write_push(CONSTANT, ord(ch))
            writer.write_call('String.appendChar', 2)

    elif token in KEYWORD_CONSTANTS:
        if token == THIS:
            writer.write_push(POINTER, 0)
        elif token == TRUE:
            writer.write_push(CONSTANT, 0)
            writer.write('not')
        elif token == FALSE:
            writer.write_push(CONSTANT, 0)
        elif token == NULL:
            writer.write_push(CONSTANT, 0)
    elif next_token == '[':
        var_name = token  # varName
        if var_name in class_symbol_table:
            var_scope, _, var_index = class_symbol_table[var_name]
        else:
            var_scope, _, var_index = subroutine_symbol_table[var_name]
        memory_segment = scope_to_segment(var_scope)
        writer.write_push(memory_segment, var_index)
        assert tokenizer.pop() == (SYMBOL, '[')  # [
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        assert tokenizer.pop() == (SYMBOL, ']')  # ]
        writer.write('add')
        writer.write_pop(POINTER, 1)
        writer.write_push(THAT, 0)

    elif token == '(':
        # assert tokenizer.pop() == (SYMBOL, '(')  # (
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        assert tokenizer.pop() == (SYMBOL, ')')  # )
    elif token == '~':
        compile_term(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        writer.write('not')
    elif token == '-':
        compile_term(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        writer.write('neg')
    elif next_token in ['(', '.']:
        compile_subroutine_call(tokenizer,
                                writer,
                                class_symbol_table,
                                subroutine_symbol_table,
                                (token_type, token))
    else:
        scope, var_type, index = class_symbol_table[token] \
            if token in class_symbol_table else subroutine_symbol_table[token]
        segment = scope_to_segment(scope)
        writer.write_push(segment, index)


def compile_expression_list(tokenizer: Tokenizer,
                            writer: VMWriter,
                            class_symbol_table: dict,
                            subroutine_symbol_table: dict):
    num_expressions = 0
    if tokenizer.peek()[1] != ')':
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
        num_expressions += 1
        while tokenizer.peek()[1] == ',':
            assert tokenizer.pop() == (SYMBOL, ',')  # ,
            compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
            num_expressions += 1
    return num_expressions


def compile_subroutine_call(tokenizer: Tokenizer,
                            writer: VMWriter,
                            class_symbol_table: dict,
                            subroutine_symbol_table: dict,
                            args=None):
    token, name = tokenizer.pop() if args is None else args
    is_method = False
    if tokenizer.peek()[1] == '.':
        assert tokenizer.pop() == (SYMBOL, '.')  # .

        if name in class_symbol_table:
            scope, var_type, index = class_symbol_table[name]
            segment = scope_to_segment(scope)
            writer.write_push(segment, index)
            name = var_type + '.' + tokenizer.pop()[1]
            is_method = True
        elif name in subroutine_symbol_table:
            scope, var_type, index = subroutine_symbol_table[name]
            segment = scope_to_segment(scope)
            writer.write_push(segment, index)
            name = var_type + '.' + tokenizer.pop()[1]
            is_method = True
        else:
            name += '.'
            name += tokenizer.pop()[1]
    else:
        writer.write_push(POINTER, 0)
        name = CUR_CLASS_NAME + '.' + name
        is_method = True

    assert tokenizer.pop() == (SYMBOL, '(')  # (
    num_args = compile_expression_list(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    if is_method:
        num_args += 1
    assert tokenizer.pop() == (SYMBOL, ')')  # )
    writer.write_call(name, num_args)


def compile_do_statement(tokenizer: Tokenizer,
                         writer: VMWriter,
                         class_symbol_table: dict,
                         subroutine_symbol_table: dict):
    assert tokenizer.pop() == (KEYWORD, DO)  # do
    compile_subroutine_call(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    writer.write_pop(TEMP, 0)
    assert tokenizer.pop() == (SYMBOL, ';')  # ;


def compile_return_statement(tokenizer: Tokenizer,
                             writer: VMWriter,
                             class_symbol_table: dict,
                             subroutine_symbol_table: dict):
    assert tokenizer.pop() == (KEYWORD, RETURN)  # return
    if tokenizer.peek()[1] != ';':
        compile_expression(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    else:
        writer.write_push(CONSTANT, 0)
    assert tokenizer.pop() == (SYMBOL, ';')  # ;
    writer.write_return()


def compile_statement(tokenizer: Tokenizer,
                      writer: VMWriter,
                      class_symbol_table: dict,
                      subroutine_symbol_table: dict):
    next_token = tokenizer.peek()[1]
    if next_token == LET:
        compile_let_statement(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    elif next_token == IF:
        compile_if_statement(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    elif next_token == WHILE:
        compile_while_statement(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    elif next_token == DO:
        compile_do_statement(tokenizer, writer, class_symbol_table, subroutine_symbol_table)
    elif next_token == RETURN:
        compile_return_statement(tokenizer, writer, class_symbol_table, subroutine_symbol_table)


def compile_subroutine_body(tokenizer: Tokenizer,
                            writer: VMWriter,
                            class_symbol_table: dict,
                            subroutine_symbol_table: dict,
                            function_name: str,
                            subroutine_type: str,
                            class_name: str):
    assert tokenizer.pop() == (SYMBOL, '{')  # {

    while tokenizer.peek()[1] == VAR:
        compile_variable_dec(tokenizer, subroutine_symbol_table)

    n_local_vars = count_num_vars(VAR, subroutine_symbol_table)

    writer.write_function(function_name, n_local_vars)

    if subroutine_type == METHOD:
        subroutine_symbol_table[THIS] = (ARGUMENT, class_name, 0)
        writer.write_push(ARGUMENT, 0)
        writer.write_pop(POINTER, 0)

    if subroutine_type == CONSTRUCTOR:
        num_fields = count_num_vars(FIELD, class_symbol_table)
        writer.write_push(CONSTANT, num_fields)
        writer.write_call('Memory.alloc', 1)
        writer.write_pop(POINTER, 0)

    compile_statements(tokenizer, writer, class_symbol_table, subroutine_symbol_table)

    assert tokenizer.pop() == (SYMBOL, '}')  # }


def compile_statements(tokenizer: Tokenizer,
                       writer: VMWriter,
                       class_symbol_table: dict,
                       subroutine_symbol_table: dict):
    while tokenizer.peek()[1] != '}':
        compile_statement(tokenizer, writer, class_symbol_table, subroutine_symbol_table)


def compile_parameter_list(tokenizer: Tokenizer,
                           subroutine_symbol_table: dict):

    num_args = len(subroutine_symbol_table)
    if tokenizer.peek()[1] != ')':
        var_type = tokenizer.pop()[1]  # type
        var_name = tokenizer.pop()[1]  # variable name
        subroutine_symbol_table[var_name] = (ARGUMENT, var_type, num_args)
        num_args += 1
        while tokenizer.peek()[1] == ',':
            assert tokenizer.pop() == (SYMBOL, ',')  # ,
            var_type = tokenizer.pop()[1]  # type
            var_name = tokenizer.pop()[1]  # variable name
            subroutine_symbol_table[var_name] = (ARGUMENT, var_type, num_args)
            num_args += 1


def compile_class_subroutine_dec(tokenizer: Tokenizer,
                                 writer: VMWriter,
                                 class_symbol_table: dict,
                                 class_name: str):
    subroutine_type = tokenizer.pop()[1]  # constructor | function | method
    tokenizer.pop()  # void | type
    function_name = class_name + '.' + tokenizer.pop()[1]  # subroutine name

    assert tokenizer.pop() == (SYMBOL, '(')  # (

    subroutine_symbol_table = {}
    if subroutine_type == METHOD:
        subroutine_symbol_table['asd'] = 'asd'

    compile_parameter_list(tokenizer, subroutine_symbol_table)

    assert tokenizer.pop() == (SYMBOL, ')')  # )

    compile_subroutine_body(tokenizer, writer, class_symbol_table, subroutine_symbol_table,
                            function_name, subroutine_type, class_name)


def compile_class(tokenizer: Tokenizer, writer: VMWriter):
    global CUR_CLASS_NAME
    assert tokenizer.pop() == (KEYWORD, CLASS)  # must be class
    class_name = tokenizer.pop()[1]     # class name
    CUR_CLASS_NAME = class_name
    assert tokenizer.pop() == (SYMBOL, '{')     # {

    class_symbol_table = {}
    while tokenizer.peek()[1] in CLASS_VAR_TYPES:
        compile_class_var_dec(tokenizer, class_symbol_table)

    while tokenizer.peek()[1] in SUBROUTINE_NAMES:
        compile_class_subroutine_dec(tokenizer, writer, class_symbol_table, class_name)

    assert tokenizer.pop() == (SYMBOL, '}')     # }


def write_vm_file(input_file: str, output_file: str):
    tokenizer = Tokenizer(input_file)
    writer = VMWriter(output_file)
    compile_class(tokenizer, writer)
    writer.close()


def parse_file(input_file: str, output_dir: str):
    output_file = get_output_file_path(input_file, output_dir)
    write_vm_file(input_file, output_file)


def get_output_file_path(input_file: str, output_dir: str):
    file_name = input_file.split('/')[-1].split('.')[0]
    out_file = output_dir + '/' + file_name + '.vm'
    return out_file


def main():
    input_files, output_dir = read_program_args()
    for input_file in input_files:
        parse_file(input_file, output_dir)


if __name__ == '__main__':
    main()
