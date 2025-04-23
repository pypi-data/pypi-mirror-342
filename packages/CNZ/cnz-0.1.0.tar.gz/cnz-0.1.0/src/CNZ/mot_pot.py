mot = {"MOVER": "01", "MOVEM": "02", "ADD": "03", "SUB": "04", "MULT": "05", "DIV": "06"}
pot = {"START", "END", "DS", "DC", "EQU", "ORIGIN"}

def is_label(word):
    return word.endswith(":")

def process_assembly(code_lines):
    print("\nMnemonic Opcode Table (MOT) Used:")
    print("{:<10}{}".format("Mnemonic", "Opcode"))
    for line in code_lines:
        words = line.strip().replace(",", "").split()
        for word in words:
            if word in mot:
                print("{:<10}{}".format(word, mot[word]))

    print("\nPseudo Opcode Table (POT) Used:")
    for line in code_lines:
        words = line.strip().split()
        for word in words:
            if word in pot:
                print(word)

def main():
    print("\nEnter ALP Code (type 'END' to finish):")
    code_lines = []
    while True:
        line = input("> ")
        code_lines.append(line)
        if "END" in line.upper():
            break
    process_assembly(code_lines)

if __name__ == "__main__":
    main()
