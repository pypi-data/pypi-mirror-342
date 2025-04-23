def identify_and_expand_macros(lines):
    mnt = {}
    mdt = []
    ala = {}
    expanded = []

    i = 0
    mdt_index = 0
    while i < len(lines):
        if lines[i].strip() == "MACRO":
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
        else:
            tokens = lines[i].split()
            if tokens and tokens[0] in mnt:
                macro = tokens[0]
                args = tokens[1:]
                mapping = {f"#ARG{j}": args[j] for j in range(len(args))}
                idx = mnt[macro]
                while mdt[idx] != "MEND":
                    temp = mdt[idx]
                    for k, v in mapping.items():
                        temp = temp.replace(k, v)
                    expanded.append(temp)
                    idx += 1
            else:
                expanded.append(lines[i])
        i += 1
    return expanded

def menu_macro_processor_3():
    print("\n--- Single Pass Macro Processor with Macro Identification ---")
    print("Enter macro + main code (END to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    expanded_code = identify_and_expand_macros(lines)
    print("\n--- Expanded Code ---")
    for line in expanded_code:
        print(line)

menu_macro_processor_3()

# MACRO
# SWAP &A, &B
# MOV R, &A
# MOV &A, &B
# MOV &B, R
# MEND
# START
# SWAP X, Y
# END
