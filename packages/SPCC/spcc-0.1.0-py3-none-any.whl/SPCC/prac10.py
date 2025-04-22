import re

# Regular expressions for different token types
regex_number = r'\b\d+(\.\d+)?\b'  # Matches integers and floating-point numbers
regex_identifier = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'  # Identifiers (starts with letter or underscore)
regex_preprocessor = r'^\s*#\s*(\w+)'  # Matches preprocessor directives starting with #

# Function to perform lexical analysis
def lexical_analyzer(code):
    tokens = []
    
    # Preprocess the code to handle different token types
    lines = code.splitlines()  # Split code into lines for easy preprocessor directive handling
    
    for line in lines:
        # Match Preprocessor Directives
        if re.match(regex_preprocessor, line):
            directive = re.match(regex_preprocessor, line).group(1)
            tokens.append(('Preprocessor Directive', directive))
        
        # Match Numbers (integers and floats)
        for match in re.finditer(regex_number, line):
            tokens.append(('Number', match.group()))
        
        # Match Identifiers
        for match in re.finditer(regex_identifier, line):
            tokens.append(('Identifier', match.group()))
    
    return tokens

# Sample input code (as a string)
code = '''
#include <stdio.h>
#define MAX 100
int main() {
    int a = 10;
    float b = 20.5;
    a = a + 2;
    if (a > b) {
        return a;
    }
}
'''

# Perform lexical analysis
tokens = lexical_analyzer(code)

# Display tokens
print("Tokens in the code:")
for token in tokens:
    print(f"Type: {token[0]}, Value: {token[1]}")
