def algebraic_simplify(expr):
    replacements = {
        "* 1": "", "+ 0": "", "- 0": "", "/ 1": "",
        "* 0": "0", "0 *": "0"
    }
    for pattern, repl in replacements.items():
        expr = expr.replace(pattern, repl)
    return expr

def eliminate_common(expr_list):
    temp_map = {}
    optimized = []
    for expr in expr_list:
        if expr in temp_map:
            optimized.append(f"{temp_map[expr]}")
        else:
            t = f"T{len(temp_map)+1}"
            temp_map[expr] = t
            optimized.append(f"{t} = {expr}")
    return optimized

def menu_optimizer1():
    while True:
        print("\n--- Code Optimization Menu [Simplification, CSE] ---")
        print("1. Algebraic Simplification")
        print("2. Common Sub-expression Elimination")
        print("3. Exit")
        ch = input("Enter choice: ")
        if ch == '1':
            expr = input("Enter expression (e.g. a = a + 0): ")
            print("Optimized:", algebraic_simplify(expr))
        elif ch == '2':
            n = int(input("Enter number of expressions: "))
            exprs = [input(f"Expr {i+1}: ") for i in range(n)]
            print("Optimized expressions:")
            for e in eliminate_common(exprs):
                print(e)
        elif ch == '3':
            break
        else:
            print("Invalid choice.")

menu_optimizer1()


# a = a + 0
# b = a + 0
