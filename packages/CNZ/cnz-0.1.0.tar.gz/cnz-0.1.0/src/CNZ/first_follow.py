from collections import defaultdict

first_sets = defaultdict(set)
follow_sets = defaultdict(set)
grammar = defaultdict(list)
non_terminals = set()
terminals = set()
start_symbol = None

def compute_first(symbol):
    if symbol in first_sets:
        return first_sets[symbol]

    first = set()

    if symbol not in non_terminals:
        first.add(symbol)
    else:
        for production in grammar[symbol]:
            if len(production) == 0 or production == ['ε'] or production == ['e'] or production == ['epsilon']:
                first.add("ε")
            else:
                for sym in production:
                    sym_first = compute_first(sym)
                    first |= sym_first - {"ε"}
                    if "ε" not in sym_first:
                        break
                else:
                    first.add("ε")

    first_sets[symbol] = first
    return first

def compute_follow(symbol):
    if symbol in follow_sets:
        return follow_sets[symbol]

    follow = set()
    if symbol == start_symbol:
        follow.add("$")

    for lhs in grammar:
        for production in grammar[lhs]:
            for i in range(len(production)):
                if production[i] == symbol:
                    beta = production[i+1:]
                    if beta:
                        first_beta = set()
                        for sym in beta:
                            first_sym = compute_first(sym)
                            first_beta |= first_sym - {"ε"}
                            if "ε" not in first_sym:
                                break
                        else:
                            follow |= compute_follow(lhs)
                        follow |= first_beta
                    else:
                        if lhs != symbol:
                            follow |= compute_follow(lhs)

    follow_sets[symbol] = follow
    return follow

def display_sets(sets):
    for non_terminal in grammar:
        print(f"{non_terminal} : {{ {', '.join(sets[non_terminal])} }}")

def input_grammar():
    global start_symbol
    print("\nEnter grammar productions (use 'ε' for epsilon and '|' for multiple rules). Type 'end' to stop:\n")
    while True:
        line = input("Production: ")
        if line.strip().lower() == "end":
            break
        if "->" not in line:
            print("Invalid format. Use A -> B.")
            continue
        lhs, rhs = line.split("->")
        lhs = lhs.strip()
        if start_symbol is None:
            start_symbol = lhs
        non_terminals.add(lhs)
        productions = rhs.strip().split("|")
        for prod in productions:
            symbols = prod.strip().split()
            grammar[lhs].append(symbols)
            for sym in symbols:
                if not sym.isupper() and sym not in ("ε", "e", "epsilon"):
                    terminals.add(sym)
                elif sym.isupper():
                    non_terminals.add(sym)

def main():
    input_grammar()
    while True:
        print("\n==== MENU ====")
        print("1. Display FIRST sets")
        print("2. Display FOLLOW sets")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            for non_terminal in grammar:
                compute_first(non_terminal)
            print("\nFIRST Sets:")
            display_sets(first_sets)

        elif choice == '2':
            for non_terminal in grammar:
                compute_first(non_terminal)
            for non_terminal in grammar:
                compute_follow(non_terminal)
            print("\nFOLLOW Sets:")
            display_sets(follow_sets)

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


# Production: E -> T E'
# Production: E' -> + T E' | ε
# Production: T -> F T'
# Production: T' -> * F T' | ε
# Production: F -> ( E ) | id
# Production: end
