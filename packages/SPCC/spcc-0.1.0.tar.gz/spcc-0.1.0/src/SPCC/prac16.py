import re

# List of symbols/operators
symbols = ['+', '-', '*', '/', '=', '(', ')', '{', '}', ';', ',', '<', '>', '==', '!=', '<=', '>=']

def remove_comments(code):
    # Remove single-line comments
    code = re.sub(r'//.*', '', code)
    # Remove multi-line comments
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    return code

def is_identifier(token):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token)

def analyze_code(code):
    code = remove_comments(code)
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|==|!=|<=|>=|[=+\-*/(){};,<>]', code)

    identifiers = []
    symbol_list = []

    print("Lexical Analysis Result:\n")

    for token in tokens:
        if token in symbols:
            symbol_list.append(token)
            print(f"Symbol/Operator: {token}")
        elif is_identifier(token):
            identifiers.append(token)
            print(f"Identifier: {token}")
        else:
            print(f"Unknown token: {token}")

    print("\nSummary:")
    print("Identifiers:", identifiers)
    print("Symbols/Operators:", symbol_list)

# Example program to analyze
program = """
// This is a single-line comment
int a = b + c;  /* multi-line
comment */
if (a > 10) {
    sum = sum + a;
}
"""

# Run the analyzer
analyze_code(program)
