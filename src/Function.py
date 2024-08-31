from SymbolTable import SymbolTable
class Function:
	def __init__(self, returnType, name):
		self.returnType = returnType
		self.name       = name
		self.statementsAstList = []
		self.intermediateCodeList = []
		self.localSymbolTable = SymbolTable()
	def setStatementsAstList(self, sastList):
		self.statementsAstList = sastList
	def getStatementsAstList(self):
		return self.statementsAstList
	def setIntermediateCodeList(self, icList):
		self.intermediateCodeList = icList
	def getIntermediateCodeList(self):
		return self.intermediateCodeList
	def setLocalSymbolTable(self,localList):
		self.localSymbolTable = localList
	def getLocalSymbolTable(self):
		return self.localSymbolTable
	def getFunctionName(self):
		return self.name
	
	def print(self):
		print(f"\tProcedure: {self.name}, Return Type: {self.returnType}\n")
		for statement in self.statementsAstList:
			statement.print()

	def printIntermediate(self):
		print(f'{self.name}:')
		for statement in self.intermediateCodeList:
			statement.print()