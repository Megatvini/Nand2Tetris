import argparse
import os

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


class XMLWriter:
    def __init__(self, output_file: str):
        self._out_file = open(output_file, 'w')

    def open_tag(self, tag_name: str, newline=False):
        self._out_file.write('<{}>'.format(tag_name))
        if newline:
            self._out_file.write('\n')

    def close_tag(self, tag_name: str):
        self._out_file.write('</{}>\n'.format(tag_name))

    def write_value(self, value: str):
        self._out_file.write(
            value
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace("'", '&apos;')
            .replace('"', '&quot;')
        )

    def write_tag_with_value(self, tag_name: str, value: str, newline=False):
        self.open_tag(tag_name, newline)
        self.write_value(value)
        self.close_tag(tag_name)

    def close(self):
        self._out_file.close()


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


def find_all(x: str, substr: str) -> list:
    indices = []
    found = x.find(substr)
    while found != -1:
        indices.append(found)
        found = x.find(substr, found + 1)
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


def write_token_file(input_file: str, output_file: str):
    writer = XMLWriter(output_file)
    tokenizer = Tokenizer(input_file)
    writer.open_tag(TOKENS, newline=True)

    while not tokenizer.is_empty():
        token_type, token = tokenizer.pop()
        writer.open_tag(token_type)
        writer.write_value(token)
        writer.close_tag(token_type)

    writer.close_tag(TOKENS)
    writer.close()


def compile_class_var_dec(tokenizer: Tokenizer, writer: XMLWriter):
    writer.write_tag_with_value(*tokenizer.pop())  # static | field
    writer.write_tag_with_value(*tokenizer.pop())  # type
    writer.write_tag_with_value(*tokenizer.pop())  # variable name
    while tokenizer.peek()[1] == ',':
        writer.write_tag_with_value(*tokenizer.pop())  # ,
        writer.write_tag_with_value(*tokenizer.pop())  # variable name
    writer.write_tag_with_value(*tokenizer.pop())  # ;


def compile_variable_dec(tokenizer: Tokenizer, writer: XMLWriter):
    writer.write_tag_with_value(*tokenizer.pop())  # var
    writer.write_tag_with_value(*tokenizer.pop())  # type
    writer.write_tag_with_value(*tokenizer.pop())  # varName
    while tokenizer.peek()[1] == ',':
        writer.write_tag_with_value(*tokenizer.pop())  # ,
        writer.write_tag_with_value(*tokenizer.pop())  # varName

    writer.write_tag_with_value(*tokenizer.pop())  # ;


def compile_expression(tokenizer, writer):
    writer.open_tag(EXPRESSION, newline=True)
    compile_term(tokenizer, writer)
    while tokenizer.peek()[1] in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
        writer.write_tag_with_value(*tokenizer.pop())  # op
        compile_term(tokenizer, writer)
    writer.close_tag(EXPRESSION)


def compile_let_statement(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(LET_STATEMENT, newline=True)
    writer.write_tag_with_value(*tokenizer.pop())  # let
    writer.write_tag_with_value(*tokenizer.pop())  # varName
    if tokenizer.peek()[1] == '[':
        writer.write_tag_with_value(*tokenizer.pop())  # [
        compile_expression(tokenizer, writer)
        writer.write_tag_with_value(*tokenizer.pop())  # ]

    writer.write_tag_with_value(*tokenizer.pop())  # =
    compile_expression(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # ;
    writer.close_tag(LET_STATEMENT)


def compile_if_statement(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(IF_STATEMENT, newline=True)
    writer.write_tag_with_value(*tokenizer.pop())  # if
    writer.write_tag_with_value(*tokenizer.pop())  # (
    compile_expression(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # )
    writer.write_tag_with_value(*tokenizer.pop())  # {
    compile_statements(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # }
    if tokenizer.peek()[1] == 'else':
        writer.write_tag_with_value(*tokenizer.pop())  # else
        writer.write_tag_with_value(*tokenizer.pop())  # {
        compile_statements(tokenizer, writer)
        writer.write_tag_with_value(*tokenizer.pop())  # }
    writer.close_tag(IF_STATEMENT)


def compile_while_statement(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(WHILE_STATEMENT, newline=True)
    writer.write_tag_with_value(*tokenizer.pop())  # while
    writer.write_tag_with_value(*tokenizer.pop())  # (
    compile_expression(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # )
    writer.write_tag_with_value(*tokenizer.pop())  # {
    compile_statements(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # }
    writer.close_tag(WHILE_STATEMENT)


def compile_term(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(TERM, newline=True)
    token_type, token = tokenizer.pop()
    next_token_type, next_token = tokenizer.peek()
    if is_number(token):
        writer.write_tag_with_value(INTEGER_CONSTANT, token)
    elif token_type == STRING_CONSTANT:
        writer.write_tag_with_value(STRING_CONSTANT, token)
    elif token in KEYWORD_CONSTANTS:
        writer.write_tag_with_value(token_type, token)
    elif next_token == '[':
        writer.write_tag_with_value(token_type, token)  # varName
        writer.write_tag_with_value(*tokenizer.pop())  # [
        compile_expression(tokenizer, writer)
        writer.write_tag_with_value(*tokenizer.pop())  # ]
    elif token == '(':
        writer.write_tag_with_value(token_type, token)  # (
        compile_expression(tokenizer, writer)
        writer.write_tag_with_value(*tokenizer.pop())  # )
    elif next_token in ['(', '.']:
        compile_subroutine_call(tokenizer, writer, (token_type, token))
    elif token in ['-', '~']:
        writer.write_tag_with_value(token_type, token)  # - | ~
        compile_term(tokenizer, writer)
    else:
        writer.write_tag_with_value(token_type, token)  # varName
    writer.close_tag(TERM)


def compile_expression_list(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(EXPRESSION_LIST, newline=True)
    if tokenizer.peek()[1] != ')':
        compile_expression(tokenizer, writer)
        while tokenizer.peek()[1] == ',':
            writer.write_tag_with_value(*tokenizer.pop())  # ,
            compile_expression(tokenizer, writer)
    writer.close_tag(EXPRESSION_LIST)


def compile_subroutine_call(tokenizer, writer, args=None):
    token, name = tokenizer.pop() if args is None else args

    writer.write_tag_with_value(token, name)
    if tokenizer.peek()[1] != '.':
        writer.write_tag_with_value(*tokenizer.pop())  # (
        compile_expression_list(tokenizer, writer)
        writer.write_tag_with_value(*tokenizer.pop())  # )
    else:
        writer.write_tag_with_value(*tokenizer.pop())  # .
        writer.write_tag_with_value(*tokenizer.pop())  # subroutineName
        writer.write_tag_with_value(*tokenizer.pop())  # (
        compile_expression_list(tokenizer, writer)
        writer.write_tag_with_value(*tokenizer.pop())  # )


def compile_do_statement(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(DO_STATEMENT, newline=True)
    writer.write_tag_with_value(*tokenizer.pop())  # do
    compile_subroutine_call(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # ;
    writer.close_tag(DO_STATEMENT)


def compile_return_statement(tokenizer: Tokenizer, writer: XMLWriter):
    writer.open_tag(RETURN_STATEMENT, newline=True)
    writer.write_tag_with_value(*tokenizer.pop())  # return
    if tokenizer.peek()[1] != ';':
        compile_expression(tokenizer, writer)
    writer.write_tag_with_value(*tokenizer.pop())  # ;
    writer.close_tag(RETURN_STATEMENT)


def compile_statement(tokenizer: Tokenizer, writer: XMLWriter):
    next_token = tokenizer.peek()[1]
    if next_token == LET:
        compile_let_statement(tokenizer, writer)
    elif next_token == IF:
        compile_if_statement(tokenizer, writer)
    elif next_token == WHILE:
        compile_while_statement(tokenizer, writer)
    elif next_token == DO:
        compile_do_statement(tokenizer, writer)
    elif next_token == RETURN:
        compile_return_statement(tokenizer, writer)


def compile_subroutine_body(tokenizer: Tokenizer, writer: XMLWriter):
    writer.write_tag_with_value(*tokenizer.pop())  # {
    while tokenizer.peek()[1] == VAR:
        writer.open_tag(VAR_DEC, newline=True)
        compile_variable_dec(tokenizer, writer)
        writer.close_tag(VAR_DEC)

    compile_statements(tokenizer, writer)

    writer.write_tag_with_value(*tokenizer.pop())  # }


def compile_statements(tokenizer, writer):
    writer.open_tag(STATEMENTS, newline=True)
    while tokenizer.peek()[1] != '}':
        compile_statement(tokenizer, writer)
    writer.close_tag(STATEMENTS)


def compile_parameter_list(tokenizer: Tokenizer, writer: XMLWriter):
    if tokenizer.peek()[1] != ')':
        writer.write_tag_with_value(*tokenizer.pop())  # type
        writer.write_tag_with_value(*tokenizer.pop())  # variable name
        while tokenizer.peek()[1] == ',':
            writer.write_tag_with_value(*tokenizer.pop())  # ,
            writer.write_tag_with_value(*tokenizer.pop())  # type
            writer.write_tag_with_value(*tokenizer.pop())  # variable name


def compile_class_subroutine_dec(tokenizer: Tokenizer, writer: XMLWriter):
    writer.write_tag_with_value(*tokenizer.pop())  # constructor | function | method
    writer.write_tag_with_value(*tokenizer.pop())  # void | type
    writer.write_tag_with_value(*tokenizer.pop())  # subroutine name
    writer.write_tag_with_value(*tokenizer.pop())  # (
    writer.open_tag(PARAMETER_LIST, newline=True)
    compile_parameter_list(tokenizer, writer)
    writer.close_tag(PARAMETER_LIST)
    writer.write_tag_with_value(*tokenizer.pop())  # )

    writer.open_tag(SUBROUTINE_BODY, newline=True)
    compile_subroutine_body(tokenizer, writer)
    writer.close_tag(SUBROUTINE_BODY)


def compile_class(tokenizer: Tokenizer, writer: XMLWriter):
    writer.write_tag_with_value(*tokenizer.pop())  # must be class
    writer.write_tag_with_value(*tokenizer.pop())  # class name
    writer.write_tag_with_value(*tokenizer.pop())  # {

    while tokenizer.peek()[1] in CLASS_VAR_TYPES:
        writer.open_tag(CLASS_VAR_DEC, newline=True)
        compile_class_var_dec(tokenizer, writer)
        writer.close_tag(CLASS_VAR_DEC)

    while tokenizer.peek()[1] in SUBROUTINE_NAMES:
        writer.open_tag(SUBROUTINE_DEC, newline=True)
        compile_class_subroutine_dec(tokenizer, writer)
        writer.close_tag(SUBROUTINE_DEC)

    writer.write_tag_with_value(*tokenizer.pop())  # }


def write_out_file(input_file: str, output_file: str):
    writer = XMLWriter(output_file)
    writer.open_tag(CLASS, newline=True)
    tokenizer = Tokenizer(input_file)
    compile_class(tokenizer, writer)
    writer.close_tag(CLASS)
    writer.close()


def parse_file(input_file: str, output_dir: str):
    output_token_file, output_file = get_output_file_path(input_file, output_dir)
    write_token_file(input_file, output_token_file)
    write_out_file(input_file, output_file)


def get_output_file_path(input_file: str, output_dir: str):
    file_name = input_file.split('/')[-1].split('.')[0]
    out_token_file = output_dir + '/' + file_name + 'T.xml'
    out_file = output_dir + '/' + file_name + '.xml'
    return out_token_file, out_file


def main():
    input_files, output_dir = read_program_args()
    for input_file in input_files:
        parse_file(input_file, output_dir)


if __name__ == '__main__':
    main()
