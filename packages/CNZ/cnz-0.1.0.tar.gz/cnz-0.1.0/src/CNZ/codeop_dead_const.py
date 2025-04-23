import re


def dead_code_elimination(code_lines):
    used_vars = set()
    optimized = []

    for line in reversed(code_lines):
        parts = line.split('=')
        if len(parts) == 2:
            var, expr = parts[0].strip(), parts[1].strip()
            if var in used_vars or 'print' in expr:
                optimized.insert(0, line)
                used_vars.update(re.findall(r'\b[a-zA-Z_]\w*\b', expr))
        else:
            optimized.insert(0, line)
    return optimized

def constant_propagation(code_lines):
    const_table = {}
    optimized = []

    for line in code_lines:
        if '=' in line:
            var, expr = map(str.strip, line.split('='))
            if expr.isdigit():
                const_table[var] = expr
                optimized.append(f"{var} = {expr}")
            else:
                for k, v in const_table.items():
                    expr = expr.replace(k, v)
                optimized.append(f"{var} = {expr}")
        else:
            optimized.append(line)
    return optimized

def menu_optimizer2():
    while True:
        print("\n--- Code Optimization Menu [Dead Code, Constant Propagation] ---")
        print("1. Dead Code Elimination")
        print("2. Constant Propagation")
        print("3. Exit")
        ch = input("Enter choice: ")
        if ch == '1':
            n = int(input("Enter number of lines: "))
            code = [input(f"Line {i+1}: ") for i in range(n)]
            result = dead_code_elimination(code)
            print("Optimized Code:")
            for line in result:
                print(line)
        elif ch == '2':
            n = int(input("Enter number of lines: "))
            code = [input(f"Line {i+1}: ") for i in range(n)]
            result = constant_propagation(code)
            print("Optimized Code:")
            for line in result:
                print(line)
        elif ch == '3':
            break
        else:
            print("Invalid choice.")

menu_optimizer2()

# The code snippet `a = 5, b = 10, c = a + b, d = 2, print(c)` is performing the following actions:
# a = 5
# b = 10
# c = a + b
# d = 2
# print(c)
