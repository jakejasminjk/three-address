with open('code.asm', 'w') as file: 
        file.write('global main\n')
        file.write('extern printf\n')
        file.write('extern sleep\n')
        file.write('section .data\n')

def writeDef(line):
    prop = line.split()
    with open('code.asm', 'a') as file:
        if(prop[0] == "INT"):
            text = "{int} dq {val}\n".format(int = prop[1], val = prop[2])
            file.write(text)
        if(prop[0] == "CHAR"):
            text = "{int} db {val} {val2} {val3}, 0\n".format(int = prop[1], val = prop[2], val2 = prop[3], val3 = prop[4])
            file.write(text)
        if(prop[0] == "FLOAT"):
            text = "{int} dq {val}\n".format(int = prop[1], val = prop[2])
            file.write(text)
         
def writeCode(line, label):
    prop = line.split()
    with open('code.asm', 'a') as f:
        if(prop[0] == "MOV"):
            labelText = "L{n}\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[2])
        elif(prop[0] == "GOTO"):
            labelText = "L{n}\n".format(n = label)
            f.write(labelText)
            text = "jmp L{val}\n".format( val = prop[1])
        elif(prop[0] == "JUMP"):
            print(prop[0])
        elif(prop[0] == "MASK"):
            print(prop[0])
        elif(prop[0] == "INC"):
            print(prop[0])
        elif(prop[0] == "DEC"):
            print(prop[0])
        elif(prop[0] == "ADD"):
            print(prop[0])
        elif(prop[0] == "SUB"):
            print(prop[0])
        elif(prop[0] == "NEG"):
            print(prop[0])
        elif(prop[0] == "PRINT"):
            print(prop[0])
        elif(prop[0] == "SLEEP"):
            print("sup")







count = 0

with open("newCode.txt", 'r') as fp:
    for line in fp:
        count += 1
        deck = line.split()
        if(deck[0] == "INT" or deck[0] == "FLOAT" or deck[0] == "CHAR"):
            writeDef(line)
        else:
            print(line)
            writeCode(line, count)

