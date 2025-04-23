def generate_quadruples(expression):
    operators = ['+', '-', '*', '/', '=']
    quadruples = []
    temp_count = 1

    tokens = expression.replace("=", " = ").replace("+", " + ").replace("-", " - ") \
                       .replace("*", " * ").replace("/", " / ").split()

    # Handle assignment first
    if '=' in tokens:
        idx = tokens.index('=')
        target = tokens[idx - 1]
        exp_tokens = tokens[idx + 1:]

        while len(exp_tokens) > 1:
            op_index = -1
            for op in ['*', '/', '+', '-']:
                if op in exp_tokens:
                    op_index = exp_tokens.index(op)
                    break

            arg1 = exp_tokens[op_index - 1]
            op = exp_tokens[op_index]
            arg2 = exp_tokens[op_index + 1]
            result = f"T{temp_count}"
            temp_count += 1
            quadruples.append((op, arg1, arg2, result))
            exp_tokens = exp_tokens[:op_index - 1] + [result] + exp_tokens[op_index + 2:]

        # Final assignment
        quadruples.append(('=', exp_tokens[0], None, target))

    return quadruples

def display_quadruples(quadruples):
    print("\nQuadruples (Op, Arg1, Arg2, Result):")
    for i, (op, arg1, arg2, res) in enumerate(quadruples):
        print(f"{i}: ({op}, {arg1}, {arg2}, {res})")

def menu_quadruples():
    while True:
        print("\n=== Quadruple Code Generator Menu ===")
        print("1. Generate Quadruples from Expression")
        print("2. Exit")
        ch = input("Enter choice: ")

        if ch == '1':
            exp = input("Enter expression (e.g., a = b + c * d): ")
            quadruples = generate_quadruples(exp)
            display_quadruples(quadruples)
        elif ch == '2':
            break
        else:
            print("Invalid choice.")

menu_quadruples()
