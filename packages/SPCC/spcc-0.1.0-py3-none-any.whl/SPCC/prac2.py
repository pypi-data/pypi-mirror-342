# Sample opcode table
MOT = {
    "L": "01", "A": "02", "ST": "03", "MOVER": "04", "MOVEM": "05", "ADD": "06", "SUB": "07"
}

POT = ["START", "END", "LTORG", "ORIGIN", "EQU"]

# Sample ALP code
alp_code = [
    "START 100",
    "LOOP  MOVER AREG, ONE",
    "       ADD   AREG, TWO",
    "       MOVEM AREG, THREE",
    "       L     BREG, FOUR",
    "       A     BREG, FIVE",
    "       ST    BREG, RESULT",
    "       END"
]

symbol_table = {}
base_table = {}
intermediate_code = []

location_counter = 0
start_address = 0
reg_map = {"AREG": 1, "BREG": 2, "CREG": 3, "DREG": 4}


# ---------- PASS 1 ----------
print("\n=== PASS 1 ===")
for line in alp_code:
    tokens = line.strip().split()
    
    if tokens[0] == "START":
        start_address = int(tokens[1])
        location_counter = start_address
        intermediate_code.append((location_counter, "START", ""))
        continue
    
    if tokens[0] == "END":
        intermediate_code.append((location_counter, "END", ""))
        break

    if len(tokens) == 3:
        label, opcode, operand = tokens
        symbol_table[label] = location_counter
    else:
        label = None
        opcode = tokens[0]
        operand = tokens[1]
    
    intermediate_code.append((location_counter, opcode, operand))
    location_counter += 1


# ---------- Generate Base Table ----------
print("\n=== BASE TABLE ===")
for reg, code in reg_map.items():
    base_table[reg] = f"Base Register {code} Initialized"

for reg, info in base_table.items():
    print(f"{reg} -> {info}")


# ---------- PASS 2 ----------
print("\n=== PASS 2 ===")
machine_code = []
for loc, opcode, operand in intermediate_code:
    if opcode in MOT:
        op_code = MOT[opcode]
        reg, sym = operand.split(",")
        address = symbol_table.get(sym.strip(), 0)
        machine_code.append((loc, op_code, reg_map[reg.strip()], address))
    elif opcode in POT:
        machine_code.append((loc, opcode, operand))


# ---------- SYMBOL TABLE ----------
print("\n=== SYMBOL TABLE ===")
for symbol, addr in symbol_table.items():
    print(f"{symbol} : {addr}")


# ---------- INTERMEDIATE CODE ----------
print("\n=== INTERMEDIATE CODE ===")
for entry in intermediate_code:
    print(entry)


# ---------- FINAL MACHINE CODE ----------
print("\n=== FINAL MACHINE CODE ===")
for code in machine_code:
    print(code)
