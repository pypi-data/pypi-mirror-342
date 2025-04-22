import re

symbol_table = {}
literal_table = []
intermediate_code = []

location_counter = 0

# Define instructions for reference (simplified)
instructions = ['START', 'END', 'DS', 'DC', 'MOVER', 'MOVEM', 'ADD', 'SUB', 'JMP']

# Pass 1: Build symbol and literal tables
def pass_one(alp_lines):
    global location_counter
    literal_pool = []

    for line in alp_lines:
        parts = line.strip().split()
        if not parts:
            continue

        if parts[0] == 'START':
            location_counter = int(parts[1])
            continue

        label = None
        if parts[0] not in instructions:
            label = parts[0]
            parts = parts[1:]

        opcode = parts[0]

        # Handle literal
        if len(parts) > 1 and "='" in parts[1]:
            literal = parts[1].split(',')[-1]
            literal_value = literal.strip()
            if literal_value not in literal_table:
                literal_table.append(literal_value)

        if label:
            if label not in symbol_table:
                symbol_table[label] = location_counter

        if opcode == 'DS':
            location_counter += int(parts[1])
        else:
            location_counter += 1

# Display Symbol and Literal Tables
def display_tables():
    print("SYMBOL TABLE:")
    print(f"{'Symbol':<10} {'Address':<10}")
    for symbol, addr in symbol_table.items():
        print(f"{symbol:<10} {addr:<10}")

    print("\nLITERAL TABLE:")
    print(f"{'Literal':<10} {'Address':<10}")
    literal_address = location_counter
    for literal in literal_table:
        print(f"{literal:<10} {literal_address:<10}")
        literal_address += 1

# Sample ALP Code
alp_code = [
    "START 100",
    "MOVER AREG, ='5'",
    "ADD BREG, ONE",
    "ONE DS 1",
    "LOOP SUB AREG, ='1'",
    "     JMP LOOP",
    "     END"
]

# Run Two-Pass Assembler Simulation
pass_one(alp_code)
display_tables()
