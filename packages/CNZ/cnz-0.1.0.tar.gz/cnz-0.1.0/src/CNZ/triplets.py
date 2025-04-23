def generate_triples(expression):
    operators = ['+', '-', '*', '/', '=']
    triples = []

    tokens = expression.replace("=", " = ").replace("+", " + ").replace("-", " - ") \
                       .replace("*", " * ").replace("/", " / ").split()

    while '=' in tokens:
        idx = tokens.index('=')
        target = tokens[idx - 1]
        left = tokens[idx + 1]
        op = tokens[idx + 2]
        right = tokens[idx + 3]

        triples.append((op, left, right))
        tokens = [target] + tokens[idx + 4:]
        tokens[1] = f'({triples.index((op, left, right)) + 100})'

    while len(tokens) > 1:
        left = tokens[0]
        op = tokens[1]
        right = tokens[2]
        triples.append((op, left, right))
        tokens = [f'({triples.index((op, left, right)) + 100})'] + tokens[3:]

    return triples

def display_triples(triples):
    print("\nTriples (Index, Operator, Arg1, Arg2):")
    for idx, (op, arg1, arg2) in enumerate(triples, start=100):
        print(f"{idx}: ({op}, {arg1}, {arg2})")

def menu_triples():
    while True:
        print("\n=== Triple Code Generator Menu ===")
        print("1. Generate Triples from Expression")
        print("2. Exit")
        ch = input("Enter choice: ")

        if ch == '1':
            exp = input("Enter expression (e.g., a = b + c * d): ")
            triples = generate_triples(exp)
            display_triples(triples)
        elif ch == '2':
            break
        else:
            print("Invalid choice.")

menu_triples()
