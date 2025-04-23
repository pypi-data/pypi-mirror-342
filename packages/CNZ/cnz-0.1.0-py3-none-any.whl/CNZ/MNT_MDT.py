def macro_expansion_pass(mnt, mdt, ala, code):
    expanded_code = []
    for line in code:
        tokens = line.strip().split()
        if tokens and tokens[0] in mnt:
            macro_name = tokens[0]
            args = tokens[1:]
            formal_args = ala[macro_name]

            # Argument mapping
            arg_map = {f"#ARG{i}": val for i, val in enumerate(args)}

            mdt_index = mnt[macro_name]
            while mdt[mdt_index] != "MEND":
                expanded_line = mdt[mdt_index]
                for k, v in arg_map.items():
                    expanded_line = expanded_line.replace(k, v)
                expanded_code.append(expanded_line)
                mdt_index += 1
        else:
            expanded_code.append(line)
    return expanded_code

def menu_macro_processor_2():
    print("\n--- Single Pass Macro Processor ---")

    # Predefined MDT, MNT, ALA
    mnt = {'INCR': 0}
    mdt = ['ADD #ARG0, =1', 'MEND']
    ala = {'INCR': ['A']}

    print("Enter code with macro calls (END to finish):")
    code = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        code.append(line)

    expanded = macro_expansion_pass(mnt, mdt, ala, code)

    print("\n--- Macro Expansion ---")
    for line in expanded:
        print(line)

menu_macro_processor_2()


# START
# INCR A
# MOV B, A
# END
