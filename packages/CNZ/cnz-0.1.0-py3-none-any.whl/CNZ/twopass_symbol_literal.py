import re

symbol_table = {}
literal_table = []
location_counter = 0
intermediate_code = []

def is_label(token):
    return token.endswith(":")

def is_literal(token):
    return token.startswith("=")

def process_line(line):
    global location_counter
    tokens = line.strip().split()

    if not tokens:
        return

    # Handle label
    if is_label(tokens[0]):
        label = tokens[0][:-1]
        if label not in symbol_table:
            symbol_table[label] = location_counter
        tokens = tokens[1:]

    if not tokens:
        return

    instruction = tokens[0].upper()

    if instruction == "START":
        if len(tokens) > 1:
            location_counter = int(tokens[1])
        else:
            location_counter = 0

    elif instruction == "END":
        # Assign addresses to literals
        for i, literal in enumerate(literal_table):
            if literal["address"] is None:
                literal["address"] = location_counter
                location_counter += 1

    else:
        # Assume normal instruction, increment location counter
        for tok in tokens[1:]:
            if is_literal(tok):
                if not any(lit["literal"] == tok for lit in literal_table):
                    literal_table.append({"literal": tok, "address": None})
        location_counter += 1

def display_symbol_table():
    print("\nSymbol Table:")
    print("{:<10}{}".format("Symbol", "Address"))
    for symbol, address in symbol_table.items():
        print("{:<10}{}".format(symbol, address))

def display_literal_table():
    print("\nLiteral Table:")
    print("{:<10}{}".format("Literal", "Address"))
    for lit in literal_table:
        print("{:<10}{}".format(lit["literal"], lit["address"]))

def input_assembly_code():
    print("\nEnter Assembly Language Program (type 'END' to finish input):\n")
    while True:
        line = input("> ")
        intermediate_code.append(line)
        process_line(line)
        if "END" in line.upper():
            break

def main():
    while True:
        print("\n==== MENU ====")
        print("1. Enter Assembly Code")
        print("2. Show Symbol Table")
        print("3. Show Literal Table")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol_table.clear()
            literal_table.clear()
            intermediate_code.clear()
            input_assembly_code()

        elif choice == '2':
            display_symbol_table()

        elif choice == '3':
            display_literal_table()

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


# START 100
# LOOP: MOVER AREG, =5
#       ADD BREG, =2
#       MOVEM AREG, TEMP
# TEMP: DC 1
#       END
