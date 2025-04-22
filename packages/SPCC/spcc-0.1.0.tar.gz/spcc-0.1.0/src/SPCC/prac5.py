# Predefined Macro Name Table (MNT)
mnt = {
    "INCR": 0
}

# Predefined Macro Definition Table (MDT)
mdt = [
    "LOAD #1",
    "ADD #2",
    "STORE #1",
    "MEND"
]

# Assembly program using the macro
alp_code = [
    "START",
    "INCR A,B",
    "MOV C,D",
    "INCR X,Y",
    "END"
]

# Store expanded assembly code
expanded_code = []

# ----- PASS 2: Macro Expansion -----
for line in alp_code:
    tokens = line.strip().split()
    if not tokens:
        continue

    macro_name = tokens[0]
    args = tokens[1].split(",") if len(tokens) > 1 else []

    if macro_name in mnt:
        mdt_index = mnt[macro_name]
        # Create local ALA for this invocation
        ala = {f"#{i+1}": args[i] for i in range(len(args))}

        while mdt[mdt_index] != "MEND":
            temp_line = mdt[mdt_index]
            for key, value in ala.items():
                temp_line = temp_line.replace(key, value)
            expanded_code.append(temp_line)
            mdt_index += 1
    else:
        expanded_code.append(line)

# ----- Output Section -----
print("=== Macro Name Table (MNT) ===")
for name, index in mnt.items():
    print(f"{name} -> MDT Index: {index}")

print("\n=== Macro Definition Table (MDT) ===")
for i, line in enumerate(mdt):
    print(f"{i} : {line}")

print("\n=== Macro Expansion Output ===")
for line in expanded_code:
    print(line)
