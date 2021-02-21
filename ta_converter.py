#!/usr/bin/python3
import sys

class LineOfCode:
    __definition_directives={
        'INT':  '{0} dq {1}\n',
        'FLOAT':'{0} dq {1}\n',
        'CHAR': '{0} db {1},0\n'
    }
    __code_directives={
        'MOV':  'mov rax, {0}\n\tmov {1}, rax\n\t',
        'GOTO': 'jmp L{0}\n\t',
        'JUMP': 'mov rax, {2}\n\tcmp rax, {3}\n\tj{0} L{1}\n\t',
        'MASK': 'mov rax, {2}\n\ttest rax, {3}\n\tj{0} L{1}\n\t',
        'INC':  'mov rax, {0}\n\tinc rax\n\tmov {0}, rax\n\t',
        'DEC':  'mov rax, {0}\n\tdec rax\n\tmov {0}, rax\n\t',
        'ADD':  'mov rax, {0}\n\tadd rax, {1}\n\tmov {2}, rax\n\t',
        'SUB':  'mov rax, {0}\n\tsub rax, {1}\n\tmov {2}, rax\n\t',
        'NEG':  'mov rax, {0}\n\tneg rax\n\tmov {0}, rax\n\t',
        'PRINT':'mov rdi, {0}\n\tmov rsi, [{1}]\n\tmov rdx, {2}\n\tcall printf\n\t',
        'SLEEP':'mov rdi, {0}\n\tcall sleep\n\t',
        'BEGIN':'section .text\nmain:\n\tsub rsp, 0x28\n\t',
        'END':  'add rsp, 0x28\n\tret'
    }
    def __init__(self,line):
        self.__code=line
        self.__command="NONE"
        self.__following=""
        self.__tokens=line.split(maxsplit=1)
        try:
            self.__command=self.__tokens[0]
            self.__following=self.__tokens[1]
        except:
            pass
        self.__tokens=self.__splitToken(self.__following)
    def getToken(self,index):
        return self.__tokens[index]
    def __standardize(self,s):
        if (s==''):
            return ''
        while (s[0]==' '):
            s=s[1:]
        while (s[-1]==' ' or s[-1]=='\n'):
            s=s[:-1]
        return s

    def __splitToken(self,line):
        line=self.__standardize(line)
        if (self.isCode()):
            tmp=line.replace(',',' ').split()
        else:
            tmp=line.split(' ',1)
        i=0
        while (i<len(tmp)):
            tmp[i]=self.__standardize(tmp[i])
            if (tmp[i]==''):
                del tmp[i]
            else:
                i+=1
        return tmp
    def isCode(self):#return true if is code
        return (self.__command in LineOfCode.__code_directives)
    def isDef(self):#return true if is definition
        return (self.__command in LineOfCode.__definition_directives)
    def convertedLineOfCode(self):
        if (self.isCode()):
            return LineOfCode.__code_directives[self.__command].format(*self.__tokens)
        else:
            return LineOfCode.__definition_directives[self.__command].format(*self.__tokens)
    def setVariablesList(self,varList):
        if self.__command=="PRINT":
            return
        for i in range(len(self.__tokens)):
            if (self.__tokens[i] in varList):
                self.__tokens[i]='['+self.__tokens[i]+']'

class CodeFileCoverter:
    def __init__(self,inputFiles,outputFile):
        self.__input=inputFiles
        self.__output=outputFile
        self.__definitions=[]
        self.__codes=[]
        self.__variables=set()
    def ReadFile(self):
        locCount=0
        for fileName in self.__input:
            with open(fileName,'r') as f:
                for line in f:
                    loc = LineOfCode(line)
                    locCount+=1
                    if (loc.isCode()):
                        self.__codes.append((loc,locCount))
                    elif (loc.isDef()):
                        self.__variables.add(loc.getToken(0))
                        self.__definitions.append(loc)
    def WriteHeader(self,file):
        file.write('global main\nextern printf\nextern sleep\n')
    def WriteDefinition(self, file):
        file.write('section .data\n')
        for definition in self.__definitions:
            file.write(definition.convertedLineOfCode())
    def WriteCode(self,file):
        for code in self.__codes:
            code[0].setVariablesList(self.__variables)
            file.write('L{}:\n\t'.format(code[1]))
            file.write(code[0].convertedLineOfCode())
    def WriteBegin(self,file):
        loc = LineOfCode('BEGIN')
        file.write(loc.convertedLineOfCode())
    def WriteFile(self):
        with open(self.__output,'w') as of:
            self.WriteHeader(of)
            self.WriteDefinition(of)
            self.WriteBegin(of)
            self.WriteCode(of)


def main(argv):
    inputFiles=[]
    outputFile='code.out'
    
    class WAC(Exception):#Exception for wrong arguement calling
        pass
    try:
        for i in range(len(argv)):
            if argv[i]=='-o':
                if (i==len(argv)-1):
                    raise WAC
                else:
                    outputFile=argv[i+1]
            elif (i==0 or argv[i-1]!='-o'):
                inputFiles.append(argv[i])
        if (len(inputFiles)>2):
            raise WAC
    except WAC:
        print('Use one of the following command')
        print('ta_converter (using default file name)')
        print('ta_converter <definetion file> <code file>')
        print('ta_converter <definetion file> <code file> -o <output file>')
        print('ta_converter <input file>')
        print('ta_converter <input file> -o <output file>')
        sys.exit(2)
    if len(inputFiles)==0:
        inputFiles.append('code.inp')
    converter = CodeFileCoverter(inputFiles,outputFile)
    converter.ReadFile()
    converter.WriteFile()


if __name__ == "__main__":
    main(sys.argv[1:])