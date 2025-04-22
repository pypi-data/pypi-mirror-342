assembly_code = [
    "MACRO",
    "INCR &ARG1,&ARG2",
    "LOAD &ARG1",
    "ADD &ARG2",
    "STORE &ARG1",
    "MEND",
    "START",
    "INCR A,B",
    "END"
]

mnt = []     # Macro Name Table: list of dicts with name and MDT index
mdt = []     # Macro Definition Table: list of strings
ala_table = {}  # ALA: macro name -> list of parameters
expanded_code = []

# ---------- PASS 1: BUILD MNT, MDT, ALA ----------
i = 0
while i < len(assembly_code):
    line = assembly_code[i].strip()
    tokens = line.split()

    if tokens[0] == "MACRO":
        i += 1
        header = assembly_code[i].strip().split()
        macro_name = header[0]
        parameters = header[1].split(",") if len(header) > 1 else []
        ala_table[macro_name] = parameters
        mnt.append({"name": macro_name, "mdt_index": len(mdt)})
        i += 1

        while assembly_code[i].strip() != "MEND":
            def_line = assembly_code[i]
            for idx, param in enumerate(parameters):
                def_line = def_line.replace(param, f"#{idx+1}")
            mdt.append(def_line)
            i += 1

        mdt.append("MEND")  # Add MEND to MDT
    else:
        expanded_code.append(line)
    i += 1

# ---------- PASS 2: MACRO EXPANSION ----------
final_code = []
for line in expanded_code:
    tokens = line.strip().split()
    if not tokens:
        continue

    macro_call = tokens[0]
    args = tokens[1].split(",") if len(tokens) > 1 else []

    macro_found = next((m for m in mnt if m["name"] == macro_call), None)
    if macro_found:
        mdt_index = macro_found["mdt_index"]
        formal_params = ala_table[macro_call]
        ala_instance = {f"#{idx+1}": args[idx] for idx in range(len(args))}

        while mdt[mdt_index] != "MEND":
            expanded_line = mdt[mdt_index]
            for k, v in ala_instance.items():
                expanded_line = expanded_line.replace(k, v)
            final_code.append(expanded_line)
            mdt_index += 1
    else:
        final_code.append(line)

# ---------- DISPLAY OUTPUTS ----------
print("\n=== Macro Name Table (MNT) ===")
for idx, entry in enumerate(mnt):
    print(f"{idx}\t{entry['name']}\tMDT Index: {entry['mdt_index']}")

print("\n=== Macro Definition Table (MDT) ===")
for idx, line in enumerate(mdt):
    print(f"{idx}\t{line}")

print("\n=== Argument List Array (ALA) ===")
for macro, params in ala_table.items():
    for idx, param in enumerate(params):
        print(f"{macro} -> {param} -> #{idx+1}")

print("\n=== Final Expanded Code ===")
for line in final_code:
    print(line)
