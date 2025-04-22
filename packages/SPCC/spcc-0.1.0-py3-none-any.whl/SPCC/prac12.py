import re

# Function for Dead Code Elimination
def dead_code_elimination(statements):
    used_vars = set()
    assigned_vars = set()

    # First pass: Identify all used variables
    for statement in statements:
        parts = statement.split("=")
        if len(parts) > 1:
            # Track assigned variables
            assigned_vars.add(parts[0].strip())
            # Track used variables (ignore assignments)
            used_vars.update(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', parts[1]))

    # Second pass: Remove statements where assigned variable is not used
    optimized_statements = []
    for statement in statements:
        parts = statement.split("=")
        if len(parts) > 1 and parts[0].strip() in used_vars:
            optimized_statements.append(statement)
        elif len(parts) == 1:  # In case of expression with no assignment
            optimized_statements.append(statement)

    return optimized_statements

# Function for Constant Propagation
def constant_propagation(statements):
    const_values = {}

    # First pass: Collect constant assignments
    for statement in statements:
        parts = statement.split("=")
        if len(parts) > 1:
            var, expr = parts[0].strip(), parts[1].strip()
            # If expression is constant, store it
            if expr.isdigit() or (expr[0] == '-' and expr[1:].isdigit()):
                const_values[var] = int(expr)

    # Second pass: Replace variables with constant values
    optimized_statements = []
    for statement in statements:
        parts = statement.split("=")
        if len(parts) > 1:
            var, expr = parts[0].strip(), parts[1].strip()
            # Replace variables in expression with their constant values
            for key, value in const_values.items():
                expr = expr.replace(key, str(value))
            optimized_statements.append(f"{var} = {expr}")
        else:
            optimized_statements.append(statement)

    return optimized_statements

# Sample input code (in the form of assignments and expressions)
code = [
    "x = 5",
    "y = 10",
    "z = x + y",
    "a = 0",
    "b = a + 1",
    "c = b + 2",
    "d = z + 3",
    "x = x + 5",
    "z = 100",
    "e = z + 50"
]

# Apply Constant Propagation
code_with_constant_propagation = constant_propagation(code)

# Apply Dead Code Elimination
optimized_code = dead_code_elimination(code_with_constant_propagation)

# Display the original code
print("Original Code:")
for line in code:
    print(line)

# Display the code after constant propagation
print("\nCode After Constant Propagation:")
for line in code_with_constant_propagation:
    print(line)

# Display the optimized code after Dead Code Elimination
print("\nOptimized Code After Dead Code Elimination:")
for line in optimized_code:
    print(line)
