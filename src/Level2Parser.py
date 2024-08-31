from sly import Parser
from Level2Lexer import LexicalAnalyzer
from SymbolTable import SymbolTable, SymbolTableEntry
from IntermediateCode import *
from Program import Program
from Ast import *
from Function import Function
from enum import Enum
from SymbolTable import DataType


class Level2Parser(Parser):
    literals = LexicalAnalyzer.literals
    tokens = LexicalAnalyzer.tokens
    precedence = (
        ("left", "="),
        ('left', LOGICALOR),
        ('left', LOGICALAND),
        ("left", EQUAL, NOTEQUAL),
        ("left", "<", ">", GREATEREQUAL, LESSEQUAL),
        ("left", "+", "-"),
        ("left", "*", "/", "%"),
        ("right", UMINUS),
    )

    program = Program()
    localSymbolTable = SymbolTable()
    statementList = []
    dataType = None
    isAccepted = True


    @_(' return_type ID "(" ")" "{" statements "}" ')
    def Program(self, value):
        function = Function(value.return_type, value.ID)
        function.setIntermediateCodeList([i for i in self.statementList if i is not None])
        function.setLocalSymbolTable(self.localSymbolTable)

        self.program.addFunctionDetails(value.ID, function)

        return self.isAccepted

    @_(" INT ")
    def return_type(self, value):
        return DataType.INT
    @_(" DOUBLE ")
    def return_type(self, value):
        return DataType.DOUBLE

    @_(' statement ";" statements ')
    def statements(self, value):
        return [value.statement] + value.statements

    @_(' statement ";" ')
    def statements(self, value):
        return [value.statement]

    @_(" declaration ")
    def statement(self, value):
        pass

    @_("assignment", "print")
    def statement(self, value):
        return value[0]

    @_(" type LIST ")
    def declaration(self, value):
        pass

    @_(' ID "," LIST ')
    def LIST(self, value):
        self.localSymbolTable.addSymbol(SymbolTableEntry(value.ID, self.dataType, self.localSymbolTable.getLen(self.dataType)*-4))
        

    @_(' ID  "=" NUMBER "," LIST ')
    def LIST(self, value):
        self.localSymbolTable.addSymbol(SymbolTableEntry(value.ID, self.dataType, self.localSymbolTable.getLen(self.dataType)*-4, value.NUMBER))
    @_(' ID  "=" NUMBER ')
    def LIST(self, value):
        self.localSymbolTable.addSymbol(SymbolTableEntry(value.ID, self.dataType, self.localSymbolTable.getLen(self.dataType)*-4,value.NUMBER))
        

    @_(" ID ")
    def LIST(self, value):
        self.localSymbolTable.addSymbol(SymbolTableEntry(value.ID, self.dataType, self.localSymbolTable.getLen(self.dataType)*-4))
        

    @_(' ID "=" expr ')
    def assignment(self, value):
        if self.localSymbolTable.nameInSymbolTable(value.ID):
            lhs = Variable(self.localSymbolTable.getSymbol(value.ID))
            quad = Quadruple(OpCode.ASSIGN,lhs,value.expr)
            
            if quad is not None:
                if quad.typeCheckQuad():
                    self.statementList.append(quad)
                else:
                    print(f"Type is not matched at line {value.lineno}")
                    self.isAccepted = False
                    return None
            else:
                print(f"Symbol {value.ID} not been declared")
                self.isAccepted = False
                return
                 
        else:
            print(f"Symbol {value.ID} not been declared")
            self.isAccepted = False
            

    @_(" PRINT expr ")
    def print(self, value):
        return PrintAst(value.expr)

    @_(
        'expr "+" expr',
        'expr "-" expr',
        'expr "*" expr',
        'expr "/" expr',
        'expr "%" expr',
        'expr ">" expr',
        'expr "<" expr',
        "expr GREATEREQUAL expr",
        "expr LESSEQUAL expr",
        "expr EQUAL expr",
        "expr NOTEQUAL expr",
        "expr LOGICALAND expr",
        "expr LOGICALOR expr",
    )
    def expr(self, value):
        if value[1] == "+":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.PLUS,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "-":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.MINUS,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "*":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.MULTIPLY,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "/":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.DIVIDE,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "%":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.MOD,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == ">":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.GREATERTHAN,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "<":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.LESSTHAN,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == ">=":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.GREATEREQUAL,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "<=":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.LESSEQUAL,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "==":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.EQUAL,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "!=":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.NOTEQUAL,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "&&":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.LOGICALAND,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp
        elif value[1] == "||":
            tempname = f't{self.localSymbolTable.getTempCount()}'
            self.localSymbolTable.incrementTempCount()

            lhsDT = value.expr0.getDataType()
            rhsDT = value.expr1.getDataType()
            datatype = CheckDataType(lhsDT,rhsDT)
            temp = Variable(SymbolTableEntry(tempname, datatype,self.localSymbolTable.getLen(self.dataType)*-4))
            quad = Quadruple(OpCode.LOGICALOR,temp,value.expr0, value.expr1)
            self.statementList.append(quad)
            return temp

    @_("NUMBER")
    def expr(self, value):
        return Constant(value.NUMBER)
    @_("FLOAT")
    def expr(self, value):
        return Constant(value.FLOAT)

    @_("ID")
    def expr(self, value):
        if self.localSymbolTable.nameInSymbolTable(value.ID):
            return Variable(self.localSymbolTable.getSymbol(value.ID))
        else:
            print(f"Symbol {value.ID} not been declared")
            self.isAccepted = False
            return None

    @_('"(" expr ")"')
    def expr(self, value):
        return value.expr

    @_(' "-" NUMBER %prec UMINUS')
    def expr(self, value):
        return Constant(-value.NUMBER)

    @_(" INT ")
    def type(self, value):
        self.dataType = DataType.INT
    
    @_(" DOUBLE ")
    def type(self, value):
        self.dataType =  DataType.DOUBLE