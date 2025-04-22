import re

class QuadrupleGenerator:
    def __init__(self):
        self.temp_count = 1
        self.quadruples = []

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def precedence(self, op):
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0

    def generate(self, expression):
        # Split assignment: a = b + c * d
        var, expr = expression.split('=')
        var = var.strip()
        expr = expr.strip()

        # Convert to tokens
        tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[+\-*/()]', expr)

        # Convert to postfix using Shunting Yard Algorithm
        output = []
        stack = []

        for token in tokens:
            if token.isalnum():
                output.append(token)
            elif token in '+-*/':
                while stack and self.precedence(stack[-1]) >= self.precedence(token):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()

        while stack:
            output.append(stack.pop())

        # Generate Quadruples from postfix
        eval_stack = []

        for token in output:
            if token not in '+-*/':
                eval_stack.append(token)
            else:
                arg2 = eval_stack.pop()
                arg1 = eval_stack.pop()
                result = self.new_temp()
                self.quadruples.append((token, arg1, arg2, result))
                eval_stack.append(result)

        # Final assignment to the variable
        final_result = eval_stack.pop()
        self.quadruples.append(('=', final_result, '-', var))

    def display(self):
        print("Generated 3-Address Code (Quadruples):")
        print(f"{'Op':^8} {'Arg1':^8} {'Arg2':^8} {'Result':^8}")
        print("-" * 36)
        for quad in self.quadruples:
            print(f"{quad[0]:^8} {quad[1]:^8} {quad[2]:^8} {quad[3]:^8}")


# Example Usage
if __name__ == "__main__":
    expression = "a = b + c * d"
    generator = QuadrupleGenerator()
    generator.generate(expression)
    generator.display()
