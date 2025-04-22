import re

# Function for Algebraic Simplification
def algebraic_simplification(expression):
    # Simplify expressions: a * 1 = a, a + 0 = a, etc.
    expression = re.sub(r'(\w+) *\* 1', r'\1', expression)  # a * 1 = a
    expression = re.sub(r'(\w+) *\+ 0', r'\1', expression)  # a + 0 = a
    expression = re.sub(r'(\w+) *- \1', '0', expression)  # a + (-a) = 0
    expression = re.sub(r'(\w+) *\* 0', '0', expression)  # a * 0 = 0
    return expression

# Function for Common Subexpression Elimination
def common_subexpression_elimination(statements):
    # Track already encountered expressions
    seen_expressions = {}
    optimized_statements = []
    temp_var_count = 1  # Temporary variable counter for CSE

    for statement in statements:
        # Identify expressions in the statement
        expr = statement.split('=')[1].strip()
        
        # Check if the expression has already been seen
        if expr in seen_expressions:
            # Replace with previously computed expression
            optimized_statements.append(f"{statement.split('=')[0].strip()} = {seen_expressions[expr]}")
        else:
            # If not seen, store the expression
            temp_var = f"temp{temp_var_count}"
            seen_expressions[expr] = temp_var
            optimized_statements.append(f"{temp_var} = {expr}")
            temp_var_count += 1

    return optimized_statements

# Sample input code (in the form of arithmetic expressions)
code = [
    "x = a * b + a * b",
    "y = a * c + d",
    "z = a * b + a * b",
    "w = x + 0",
    "v = y * 1"
]

# Apply Algebraic Simplification
simplified_code = [algebraic_simplification(statement) for statement in code]

# Apply Common Subexpression Elimination
optimized_code = common_subexpression_elimination(simplified_code)

# Display Optimized Code
print("Original Code:")
for line in code:
    print(line)

print("\nSimplified Code:")
for line in simplified_code:
    print(line)

print("\nOptimized Code (After CSE):")
for line in optimized_code:
    print(line)
