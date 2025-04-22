import re

class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_count = 1
        self.triples = []

    def generate_temp(self):
        temp = f't{self.temp_count}'
        self.temp_count += 1
        return temp

    def infix_to_postfix(self, tokens):
        precedence = {'=': 1, '+': 2, '-': 2, '*': 3, '/': 3}
        output = []
        stack = []

        for token in tokens:
            if token.isalnum():
                output.append(token)
            elif token in precedence:
                while stack and precedence.get(stack[-1], 0) >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # remove '('

        while stack:
            output.append(stack.pop())

        return output

    def generate_triples(self, expression):
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+|[+\-*/=()]', expression)
        postfix = self.infix_to_postfix(tokens)

        operands_stack = []

        for token in postfix:
            if token.isalnum():
                operands_stack.append(token)
            elif token in '+-*/':
                operand2 = operands_stack.pop()
                operand1 = operands_stack.pop()
                temp = self.generate_temp()
                self.triples.append((token, operand1, operand2))
                operands_stack.append(temp)
            elif token == '=':
                operand2 = operands_stack.pop()
                operand1 = operands_stack.pop()
                self.triples.append(('=', operand1, operand2))
                operands_stack.append(operand1)

        return self.triples

    def display_triples(self):
        print("Intermediate Code (using Triples):")
        for idx, triple in enumerate(self.triples):
            print(f"({idx + 1}) {triple[0]} {triple[1]} {triple[2]}")

# Example usage
if __name__ == "__main__":
    expression = "a = b + c * d"
    code_generator = IntermediateCodeGenerator()
    code_generator.generate_triples(expression)
    code_generator.display_triples()
