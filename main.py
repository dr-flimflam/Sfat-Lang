import sys, codecs, os
from random import randint


program_filepath = sys.argv[1]


program_lines = []
program_file = codecs.open(program_filepath, "r", "utf-8")
program_lines  = [line.strip() for line in program_file.readlines()]
to_remove = []
for line in program_lines:
    if line != "":    
        if line[0] == "#":
            to_remove.append(line)
for i in to_remove:
    program_lines.remove(i)


class Stack:
    
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1
        
    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number
        
    def pop(self):
        number = self.buf[self.sp]
        self.buf[self.sp] = 0
        self.sp -= 1
        return number
    
    def top(self):
        return self.buf[self.sp]
    
    def spf(self):
        return self.sp + 1
    
program = []
token_counter = 0
label_tracker = {}
first_line = program_lines[0].split(':')
program_lines.pop(0)
if first_line[1] == "0": debug = False
elif first_line[1] == "1": debug = True
elif first_line[1] == "2": debug = int(input("מצב ניקוי תקלות?"))
stack = Stack(int(first_line[0]))
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]
    
    if opcode == "":
        continue
    
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue
    
    program.append(opcode)
    token_counter += 1
    
    if opcode == "דחוף":
        if parts[1].isnumeric():
            number = int(parts[1])
            program.append(number)
        else:
            match parts[1]:
                case 'הוצא':
                    func = stack.pop
                case 'עליון':
                    func = stack.top
                case 'גודל':
                    func = stack.spf
            program.append(func)
        token_counter += 1
    elif opcode == "הדפס":
        if parts[1].startswith("\"") or parts[1].startswith("\'"):
            string_literal = ' '.join(parts[1:])[1:-1]
            program.append(string_literal)
        else:
            match parts[1]:
                case 'הוצא':
                    func = stack.pop
                case 'עליון':
                    func = stack.top
                case 'גודל':
                    func = stack.spf
            program.append(func)
        token_counter += 1
    elif opcode == "שווה":
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "גדול":
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "קפוץ":
        label = parts[1]
        program.append(label)
        token_counter += 1
        
    
    
pc = 0
last_goto = 0

while program[pc] != "עצור":
    
    opcode = program[pc]
    if debug: print(opcode)
    pc += 1
    if opcode == "דחוף":
        if debug: print(program[pc])
        if type(program[pc]) == int:    
            number = program[pc]
        else:
            number = int(program[pc]())
        pc += 1
        stack.push(number)
    elif opcode == "הוצא":
        stack.pop()
    elif opcode == "חבר":
        a = stack.pop()
        b = stack.pop()
        stack.push(a+b)
    elif opcode == "כפול":
        a = stack.pop()
        b = stack.pop()
        stack.push(a*b)
    elif opcode == "חלק":
        a = stack.pop()
        b = stack.pop()
        stack.push(int(a/b))
        stack.push(a%b)
    elif opcode == "מנה":
        a = stack.pop()
        b = stack.pop()
        stack.push(int(b/a))
        stack.push(b%a)
    elif opcode == "חסר":
        a = stack.pop()
        b = stack.pop()
        stack.push(a-b)
    elif opcode == "הבדל":
        a = stack.pop()
        b = stack.pop()
        stack.push(b-a)
    elif opcode == "טווח":
        a = stack.pop()
        b = stack.pop()
        if a<b:
            for i in range(a,b+1):
                stack.push(i)
        else:
            for i in range(b,a+1):
                stack.push(i)
    elif opcode == "אקראי":
        a = stack.pop()
        b = stack.pop()
        stack.push(randint(a,b))
    elif opcode == "הדפס":
        if debug: print(program[pc])
        if type(program[pc]) == str:    
            string_literal = ">>"+program[pc]
        else:
            string_literal = ">>"+str(program[pc]())
        pc += 1
        print(string_literal)
    elif opcode == "קרא":
        i = input("<<")
        if i == '': break
        number = int(i)
        stack.push(number)
    elif opcode == "שווה":
        number = stack.top()
        if debug: print(program[pc])
        if number == 0:
            last_goto = pc+1
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "גדול":
        number = stack.top()
        if debug: print(program[pc])
        if number > 0:
            last_goto = pc+1
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "קפוץ":
        number = stack.top()    
        if debug: print(program[pc])
        last_goto = pc+1
        pc = label_tracker[program[pc]]
    elif opcode == "החלף":
        i = stack.pop()
        stack.buf[stack.sp], stack.buf[i] = stack.buf[i], stack.buf[stack.sp]
    elif opcode == "חזור":
        pc = last_goto
    elif opcode == "נקה":
        os.system('cls')
    
    
    if debug: 
        print(stack.buf[0:stack.sp+1], '\n')
#print(stack.buf)