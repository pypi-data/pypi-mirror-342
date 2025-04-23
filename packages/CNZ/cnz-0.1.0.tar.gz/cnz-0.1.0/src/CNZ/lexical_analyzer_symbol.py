import re

keywords = {"int", "float", "char", "if", "else", "while", "return", "void", "for"}
symbols = {'+', '-', '*', '/', '=', '(', ')', '{', '}', ';', ',', '<', '>', '=='}

def lexical_analyzer_1(code):
    tokens = re.findall(r'\w+|[^\s\w]', code)
    for token in tokens:
        if token in keywords:
            print(f"{token} ➝ Keyword")
        elif token in symbols:
            print(f"{token} ➝ Symbol")
        elif re.match(r'^[A-Za-z_]\w*$', token):
            print(f"{token} ➝ Identifier")
        else:
            print(f"{token} ➝ Unknown")

def menu_lexer1():
    while True:
        print("\n--- Lexical Analyzer (Keywords, Identifiers, Symbols) ---")
        print("1. Analyze code")
        print("2. Exit")
        ch = input("Enter choice: ")
        if ch == '1':
            code = input("Enter code: ")
            lexical_analyzer_1(code)
        elif ch == '2':
            break
        else:
            print("Invalid choice")

menu_lexer1()

# int main() { int a = b + 1; }
