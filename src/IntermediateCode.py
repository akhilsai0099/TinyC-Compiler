from enum import Enum
from SymbolTable import DataType
OpCode = Enum("OpCode", ['ASSIGN',"PLUS", "MINUS","MULTIPLY",'DIVIDE','MOD','GREATERTHAN','LESSTHAN','GREATEREQUAL','LESSEQUAL','EQUAL','NOTEQUAL','LOGICALAND','LOGICALOR'])

class Operand:
	pass

class Variable(Operand):
	def __init__(self, symbol_entry):
		self.symbol_entry = symbol_entry

	def getDataType(self):
		return self.symbol_entry.getDataType()
	
	def get(self):
		return self.symbol_entry.getSymbolName()

	def print(self):
		return self.symbol_entry.print()

class Constant(Operand):
	def __init__(self, number):
		self.number = number

	def get(self):
		return self.number
	
	def getDataType(self):
		if isinstance(self.number, int):
			return DataType.INT
		elif isinstance(self.number, float):
			return DataType.DOUBLE
		
	def print(self):
		print(self.number, end = " ")

class Quadruple:
	def __init__(self, opcode, result, op1, op2=None):
		self.opcode = opcode
		self.result = result
		self.op1 = op1
		self.op2 = op2

	def getOp1(self):
		return self.op1.getSymbolName()
	def typeCheckQuad(self):
		if((self.result.getDataType() == self.op1.getDataType()) or (self.op2 and self.result.getDataType() == self.op2.getDataType())):
			return True
		else:
			return False
		
	def getDataType(self):
		if(self.op2 and (self.op1.getDataType() == self.op2.getDataType())):
			return self.op1.getDataType()
		
	def print(self):
		self.result.print()
		print('= ',end = "")

		self.op1.print()
		if self.op2:
			# print(self.opcode, end = " ")
			if self.opcode == OpCode.PLUS:
				print('+', end = " ")
			if self.opcode == OpCode.MINUS:
				print('-', end = " ")
			if self.opcode == OpCode.MULTIPLY:
				print('*', end = " ")
			if self.opcode == OpCode.DIVIDE:
				print('/', end = " ")
			if self.opcode == OpCode.MOD:
				print('%', end = " ")
			if self.opcode == OpCode.GREATEREQUAL:
				print('>=', end = " ")
			if self.opcode == OpCode.LESSEQUAL:
				print('<=', end = " ")
			if self.opcode == OpCode.LESSTHAN:
				print('<', end = " ")
			if self.opcode == OpCode.GREATERTHAN:
				print('>', end = " ")
			if self.opcode == OpCode.EQUAL:
				print('==', end = " ")
			self.op2.print()
		print()


def CheckDataType(lhsDT,rhsDT=None):
	if lhsDT ==  rhsDT :
		return DataType.INT
	if (lhsDT == DataType.DOUBLE and rhsDT == DataType.INT) or (lhsDT == DataType.INT and rhsDT == DataType.DOUBLE):
		return DataType.DOUBLE
	if lhsDT == DataType.DOUBLE and rhsDT == DataType.DOUBLE:
		return DataType.DOUBLE