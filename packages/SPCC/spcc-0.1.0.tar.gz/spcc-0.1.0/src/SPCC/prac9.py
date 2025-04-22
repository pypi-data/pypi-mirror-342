import re

# List of keywords in a programming language
keywords = {'if', 'else', 'while', 'for', 'return', 'int', 'float', 'char'}

# Regular expressions for different token types
regex_keywords = '|'.join(keywords)  # Keywords regex
regex_identifier = r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identifiers (starts with letter or underscore)
regex_symbol = r'[\+\-\*/\=\(\)\{\}\[\];,]'  # Symbols like operators, braces, semicolons

# Combine the regex patterns
combined_regex = f'({regex_keywords})|({regex_identifier})|({regex_symbol})'

# Function to perform lexical analysis
def lexical_analyzer(code):
    tokens = []
    # Match all tokens using the regex
    for match in re.finditer(combined_regex, code):
        if match.group(1):  # Keyword
            tokens.append(('Keyword', match.group(1)))
        elif match.group(2):  # Identifier
            tokens.append(('Identifier', match.group(2)))
        elif match.group(3):  # Symbol
            tokens.append(('Symbol', match.group(3)))
    return tokens

# Sample input code (as a string)
code = '''
int main() {
    int a = 10;
    float b = 20.5;
    if (a > b) {
        return a;
    }
    while (a < b) {
        a = a + 1;
    }
}
'''

# Perform lexical analysis
tokens = lexical_analyzer(code)

# Display tokens
print("Tokens in the code:")
for token in tokens:
    print(f"Type: {token[0]}, Value: {token[1]}")
