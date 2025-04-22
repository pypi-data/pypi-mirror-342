# Two-Pass Assembler with Symbol Table and Literal Table

MOT = { "L": "01", "A": "02", "ST": "03", "MOVER": "04", "MOVEM": "05", "ADD": "06", "SUB": "07" }
POT = ["START", "END", "LTORG", "ORIGIN", "EQU", "DS", "DC"]

alp_code = [
    "START 100",
    "LOOP MOVER AREG, ='5'",
    "     ADD AREG, VALUE",
    "     MOVEM AREG, RESULT",
    "     LTORG",
    "VALUE DC 10",
    "RESULT DS 1",
    "     END"
]

symbol_table = {}
literal_table = []
intermediate_code = []

location_counter = 0
literal_pool = []

def add_literal(lit):
    if lit not in [x['literal'] for x in literal_table]:
        literal_table.append({'literal': lit, 'address': None})

# ----------- PASS 1 ------------
print("\n=== PASS 1 ===")
for line in alp_code:
    tokens = line.strip().split()
    
    if not tokens:
        continue

    # Handle START
    if tokens[0] == "START":
        location_counter = int(tokens[1])
        intermediate_code.append((location_counter, "START", ""))
        continue

    # Handle END or LTORG
    if tokens[0] in ["END", "LTORG"]:
        # Assign addresses to literals
        for lit in literal_table:
            if lit['address'] is None:
                lit['address'] = location_counter
                location_counter += 1
        intermediate_code.append((location_counter, tokens[0], ""))
        continue

    label = ""
    opcode = ""
    operand = ""

    # Parse line
    if len(tokens) == 3:
        label, opcode, operand = tokens
    elif len(tokens) == 2:
        opcode, operand = tokens
    else:
        opcode = tokens[0]

    if label:
        symbol_table[label] = location_counter

    if operand.startswith("='"):
        add_literal(operand)

    intermediate_code.append((location_counter, opcode, operand))
    
    # Increment LC if not a declarative
    if opcode not in ["DS", "DC"]:
        location_counter += 1
    elif opcode == "DS":
        location_counter += int(operand)
    elif opcode == "DC":
        location_counter += 1


# ---------- PASS 2 (Simulated Code Gen) --------------
print("\n=== PASS 2 ===")
machine_code = []
for loc, opcode, operand in intermediate_code:
    if opcode in MOT:
        code = MOT[opcode]
        machine_code.append((loc, code, operand))
    elif opcode in POT or opcode == "START":
        machine_code.append((loc, opcode, operand))


# ---------- SYMBOL TABLE ----------
print("\n--- SYMBOL TABLE ---")
for symbol, addr in symbol_table.items():
    print(f"{symbol} : {addr}")

# ---------- LITERAL TABLE ----------
print("\n--- LITERAL TABLE ---")
for lit in literal_table:
    print(f"{lit['literal']} : {lit['address']}")

# ---------- INTERMEDIATE CODE ----------
print("\n--- INTERMEDIATE CODE ---")
for line in intermediate_code:
    print(line)

# ---------- FINAL MACHINE CODE (Simulated) ----------
print("\n--- FINAL MACHINE CODE ---")
for line in machine_code:
    print(line)
