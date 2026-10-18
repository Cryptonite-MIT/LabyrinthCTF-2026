#!/usr/local/bin/python
import re

def parse(code):
    return re.findall(r'"[^"]*"|\S+', code)

def caesar(text, shift):
    res = []
    for char in text:
        if 'a' <= char <= 'z':
            res.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            res.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            res.append(char)
    return "".join(res)

def xor(text, key):
    if not text or not key: return text
    maxlen = max(len(text), len(key))
    res = ""
    for i in range(maxlen):
        c_text = text[i % len(text)]
        c_key = key[i % len(key)]
        res += chr(ord(c_text) ^ ord(c_key))
    return res

def interpret(code, mode="sandbox", mangled_flag="", real_flag=""):
    stack = []
    
    if mode == "solve":
        stack.append(mangled_flag)

    tokens = parse(code)
    
    for token in tokens:
        try:
            if token.startswith('"') and token.endswith('"'):
                stack.append(token[1:-1])
            elif token == "DOUBLE":
                stack.append(stack[-1])
            elif token == "CROSS":
                stack[-1], stack[-2] = stack[-2], stack[-1]
            elif token == "TIE":
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif token == "SEVER":
                a = stack.pop()
                mid = (len(a) + 1) // 2
                stack.append(a[:mid])
                stack.append(a[mid:])
            elif token == "REVERSE":
                a = stack.pop()
                stack.append(a[::-1])
            elif token == "DYE":
                key = stack.pop()
                text = stack.pop()
                stack.append(xor(text, key))
            elif token == "SHIFT":
                shift_str = stack.pop()
                text = stack.pop()
                stack.append(caesar(text, int(shift_str)))
            elif token == "DRAFT":
                if mode == "sandbox":
                    user_input = input("INPUT> ")
                else:
                    user_input = input()
                stack.append(user_input)
            elif token == "INSPECT":
                val = stack.pop()
                if mode == "sandbox":
                    print(repr(val)[1:-1]) 
                elif val == real_flag:
                    print(f"Congratulations! Flag: {real_flag}")
                    return
            else:
                if mode == "sandbox":
                    print(f"Unknown instruction: {token}")
                break 
        except IndexError:
            if mode == "sandbox":
                print(f"Stack Underflow at instruction: {token}")
            break
        except ValueError:
            if mode == "sandbox":
                print(f"Invalid value at instruction: {token}")
            break

    if mode == "solve":
        print("The flag remains mangled. Try again.")

def main():
    flag = open("flag.txt", "r").readline()
    REAL_FLAG = flag.strip()
    
    mid = (len(REAL_FLAG) + 1) // 2
    left = REAL_FLAG[:mid]
    right = REAL_FLAG[mid:]
    
    left_shifted = caesar(left, 10)
    left_mangled = left_shifted[::-1]
    right_mangled = xor(right, "HADES")
    
    MANGLED_FLAG = left_mangled + right_mangled

    print("=== THE LOOM OF THE FATES ===")
    print("Welcome, mortal, to the weaving floor of the Moirai.")
    print("1. Practice at the Loom")
    print("2. Proceed forward")
    
    try:
        choice = input("> ").strip()
        
        if choice == "1":
            print("What will you weave?:")
            code = input("> ").strip()
            interpret(code, mode="sandbox")
        elif choice == "2":
            print("The thread leading you forward has been meddled with.")
            print("The Moirai in an attempt to stall you have:")
            print("  1. severed the thread, splitting it in half")
            print("  2. shifted the pattern of the left half by 10")
            print("  3. reversed the flow of the left half")
            print("  4. dyed the right half with the key \"HADES\"")
            print("  5. tied the broken ends back together")
            print("\nThe mangled thread is currently at the top of your stack.")
            print("Your journey forward will be blind. How will you untangle the thread?")
            code = input("> ").strip()
            interpret(code, mode="solve", mangled_flag=MANGLED_FLAG, real_flag=REAL_FLAG)
        else:
            print("Invalid choice.")
    except Exception:
        print("\nConnection closed.")

if __name__ == "__main__":
    main()
