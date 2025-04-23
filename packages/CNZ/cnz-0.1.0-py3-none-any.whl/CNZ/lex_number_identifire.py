import re


symbols = {'+', '-', '*', '/', '=', '<', '>', '(', ')', '{', '}', '[', ']', ';', ',', '.', ':', '!', '&', '|', '%', '^'}

def lexical_analyzer_2(code):
    lines = code.split('\n')
    for line in lines:
        if line.strip().startswith("#"):
            print(f"{line.strip()} ➝ Preprocessor Directive")
            continue
        tokens = re.findall(r'\w+|[^\s\w]', line)
        for token in tokens:
            if token.isdigit():
                print(f"{token} ➝ Number")
            elif re.match(r'^[A-Za-z_]\w*$', token):
                print(f"{token} ➝ Identifier")
            elif token in symbols:
                print(f"{token} ➝ Symbol")

def menu_lexer2():
    while True:
        print("\n--- Lexical Analyzer (Numbers, Identifiers, Preprocessor Directives) ---")
        print("1. Analyze code")
        print("2. Exit")
        ch = input("Enter choice: ")
        if ch == '1':
            code = input("Enter code:\n")
            lexical_analyzer_2(code)
        elif ch == '2':
            break
        else:
            print("Invalid choice")

menu_lexer2()

# #include<stdio.h>
# int a = 10;
