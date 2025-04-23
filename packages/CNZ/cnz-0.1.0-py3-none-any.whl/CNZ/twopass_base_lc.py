location_counter = 0
base_table = {}
intermediate_code = []

def process_line_pass1(line):
    global location_counter
    tokens = line.strip().split()

    if not tokens:
        return

    if tokens[0] == "START":
        location_counter = int(tokens[1])
        return

    elif tokens[0] == "USING":
        # Example: USING *,15 means current LC is assigned to register 15
        base_reg = tokens[1].split(",")[1]
        base_table[base_reg] = location_counter

    elif tokens[0] in ["DC", "DS"]:
        location_counter += 1

    elif len(tokens) > 1 and tokens[1] in ["DC", "DS"]:
        location_counter += 1

    elif tokens[0] == "END":
        return

    else:
        location_counter += 1

def input_assembly_code():
    print("\nEnter Assembly Language Program (type 'END' to finish input):\n")
    while True:
        line = input("> ")
        intermediate_code.append(line)
        process_line_pass1(line)
        if "END" in line.upper():
            break

def display_base_table():
    print("\nBase Table:")
    print("{:<10}{}".format("Register", "Address"))
    for reg, addr in base_table.items():
        print("{:<10}{}".format(reg, addr))

def main():
    while True:
        print("\n==== MENU ====")
        print("1. Enter Assembly Code")
        print("2. Show Base Table")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            base_table.clear()
            intermediate_code.clear()
            input_assembly_code()

        elif choice == '2':
            display_base_table()

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


# START 100
# USING *,15
# A DS 1
# B DC F'5'
# C DC F'1'
# END
