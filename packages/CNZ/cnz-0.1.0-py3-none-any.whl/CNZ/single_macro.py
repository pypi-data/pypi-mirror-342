def process_macro_definition(lines):
    mnt = {}
    mdt = []
    ala = {}
    mdt_index = 0

    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("MACRO"):
            macro_name = lines[i+1].split()[0]
            params = lines[i+1].split()[1:]
            param_names = [p.replace('&', '') for p in params]

            ala[macro_name] = param_names
            mnt[macro_name] = mdt_index

            i += 2
            while lines[i].strip() != "MEND":
                line = lines[i]
                for j, p in enumerate(param_names):
                    line = line.replace('&' + p, f"#ARG{j}")
                mdt.append(line)
                mdt_index += 1
                i += 1

            mdt.append("MEND")
            mdt_index += 1
        i += 1

    return mnt, mdt, ala

def menu_macro_processor_1():
    print("\n--- Single Macro Processor ---")
    print("Enter macro code line by line. End input with 'END':")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    mnt, mdt, ala = process_macro_definition(lines)

    print("\n--- Macro Name Table (MNT) ---")
    for name, index in mnt.items():
        print(f"{name} -> MDT Index {index}")

    print("\n--- Macro Definition Table (MDT) ---")
    for i, entry in enumerate(mdt):
        print(f"{i}:\t{entry}")

    print("\n--- Argument List Array (ALA) ---")
    for name, args in ala.items():
        print(f"{name} -> {args}")

menu_macro_processor_1()


# MACRO
# INCR &A
# ADD &A, =1
# MEND
# END
