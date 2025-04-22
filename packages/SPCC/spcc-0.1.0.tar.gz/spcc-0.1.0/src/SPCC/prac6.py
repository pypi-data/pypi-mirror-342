# Assembly Language Program with Macro Definition
alp_code = [
    "MACRO",
    "INCR &A,&B",
    "LOAD &A",
    "ADD &B",
    "STORE &A",
    "MEND",
    "START",
    "INCR X,Y",
    "MOV A,B",
    "INCR P,Q",
    "END"
]

# Tables
mnt = {}          # Macro Name Table: name -> MDT index
mdt = []          # Macro Definition Table
ala_map = {}      # Argument List Array: macro -> [&A, &B]

expanded_code = []  # Final code with macros expanded

# ---------- PASS 1: Identify and Store Macros ----------
i = 0
while i < len(alp_code):
    line = alp_code[i].strip()
    tokens = line.split()

    if tokens[0] == "MACRO":
        i += 1
        header = alp_code[i].strip().split()
        macro_name = header[0]
        args = header[1].split(",")
        mnt[macro_name] = len(mdt)
        ala_map[macro_name] = args
        i += 1

        # Process macro body
        while alp_code[i].strip() != "MEND":
            macro_line = alp_code[i]
            for idx, arg in enumerate(args):
                macro_line = macro_line.replace(arg, f"#{idx+1}")
            mdt.append(macro_line)
            i += 1

        mdt.append("MEND")  # Add MEND
    else:
        expanded_code.append(line)  # Temporarily store non-macro lines
    i += 1

# ---------- PASS 2: Expand Macros ----------
final_code = []
for line in expanded_code:
    tokens = line.strip().split()
    if not tokens:
        continue

    macro_call = tokens[0]
    if macro_call in mnt:
        # Get actual arguments and setup ALA
        actual_args = tokens[1].split(",") if len(tokens) > 1 else []
        ala_instance = {f"#{i+1}": actual_args[i] for i in range(len(actual_args))}

        # Get MDT index for macro body
        mdt_index = mnt[macro_call]
        while mdt[mdt_index] != "MEND":
            expanded_line = mdt[mdt_index]
            for key, val in ala_instance.items():
                expanded_line = expanded_line.replace(key, val)
            final_code.append(expanded_line)
            mdt_index += 1
    else:
        final_code.append(line)

# ---------- OUTPUT ----------
print("=== Macro Name Table (MNT) ===")
for name, idx in mnt.items():
    print(f"{name} -> MDT Index {idx}")

print("\n=== Macro Definition Table (MDT) ===")
for idx, line in enumerate(mdt):
    print(f"{idx}: {line}")

print("\n=== Argument List Array (ALA) ===")
for name, args in ala_map.items():
    for idx, arg in enumerate(args):
        print(f"{name} : {arg} -> #{idx+1}")

print("\n=== Final Code after Macro Expansion ===")
for line in final_code:
    print(line)
