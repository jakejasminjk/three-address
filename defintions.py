with open('code.s', 'w') as f: 
        f.write('global main\n')
        f.write('extern printf\n')
        f.write('extern sleep\n')
        n = 3
        while(n > 0):
            f.write('\n')
            n=n-1
        f.write('section .data\n')

def writeDef(line):
    prop = line.split()
    with open('code.s', 'a') as file:
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
    prop = line.replace(',','').split()
    with open('code.s', 'a') as f:
        if(prop[0] == "MOV"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[2])
            
        elif(prop[0] == "GOTO"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "jmp L{val}\n".format( val = prop[1])
            f.write(text)
            
        elif(prop[0] == "JUMP"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[3])
            f.write(text)
            text = "cmp rax, [{val}]\n".format( val = prop[4])
            f.write(text)
            text = "j{val} L{dest}\n".format( val = prop[1], dest = prop[2])
            f.write(text)
            
        elif(prop[0] == "MASK"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[3])
            f.write(text)
            text = "mov rax, [{val}]\n".format( val = prop[4])
            f.write(text)
            text = "j{val} L{dest}\n".format( val = prop[1], dest = prop[2])
            f.write(text)
            
        elif(prop[0] == "INC"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "inc rax\n"
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[1])
            f.write(text)
            
        elif(prop[0] == "DEC"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "dec rax"
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[1])
            
        elif(prop[0] == "ADD"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "add rax, [{val}]\n".format( val = prop[2])
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[3])
            
        elif(prop[0] == "SUB"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "sub rax, [{val}]\n".format( val = prop[2])
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[3])
            
        elif(prop[0] == "NEG"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rax, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "neg rax"
            f.write(text)
            text = "mov [{val}], rax\n".format( val = prop[1])
            f.write(text)
            
        elif(prop[0] == "PRINT"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rdi, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "mov rsi, [{val}]\n".format( val = prop[2])
            f.write(text)
            text = "mov rdx, [{val}]\n".format( val = prop[3])
            f.write(text)
            text = "call printf\n"
            f.write(text)
            
        elif(prop[0] == "SLEEP"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "mov rdi, [{val}]\n".format( val = prop[1])
            f.write(text)
            text = "call sleep\n"
            f.write(text)
        elif(prop[0] == "END"):
            labelText = "L{n}:\n".format(n = label)
            f.write(labelText)
            text = "add rsp, 0x28\n"
            f.write(text)
            text = "ret\n"
            f.write(text)






count = 0
secC = 0

with open("newCode.txt", 'r') as fp:
    for line in fp:
        count += 1
        deck = line.split()
        if(deck[0] == "INT" or deck[0] == "FLOAT" or deck[0] == "CHAR"):
            writeDef(line)
        else:
            if(secC == 0):
                with open('code.s', 'a') as f:
                    i = 3
                    while(i > 0):
                        f.write('\n')
                        i = i - 1
                    labelText = "section .text\n"
                    f.write(labelText)
                    text = "main:\n"
                    f.write(text)
                    text = "sub rsp, 0x28\n"
                    f.write(text)
                    secC = secC+1
           
            print(line)
            writeCode(line, count)