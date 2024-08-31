from Ast import *
from enum import Enum
DataType = Enum("DataType", ["INT", "DOUBLE"])
def generator(parser):
	program = parser.program
	function = program.getMainFunction()
	print('\t.text\t\t\t# The .text assembler directive indicates\n\t.globl main\t\t# The following is the code (as oppose to data)')
	print(f"{function.getFunctionName()}:\t\t\t\t# .globl makes main know to the outside of the program.")

	print("#Prologue begins")
	print('\tsw $ra, 0($sp)\t\t# Save the return address')
	print('\tsw $fp, -4($sp)\t\t# Save the frame pointer')
	print('\tsub $fp, $sp, 8\t\t# Update the frame pointer\n')

	localSpaceRequired = 8 + 4*function.getLocalSymbolTable().getLen(DataType.INT.name) + 8 * function.getLocalSymbolTable().getLen(DataType.DOUBLE.name)
	print(f'\tsub $sp, $sp, {localSpaceRequired}\t\t# Make space for the locals')
	print('# Prologue ends\n')
	astList = function.getStatementsAstList()
	
	for i in astList:
		if isinstance(i,AssignAst):
			if isinstance(i.right, NumberAst):
				print(f'\tli $v0, {i.right.getNumber()}')
				print(f'\tsw $v0, {i.left.getSymbolEntry().getOffset()}($fp)')

			if isinstance(i.right, NameAst):
				print(f'\tlw $v0, {i.right.getSymbolEntry().getOffset()}($fp)')
				print(f'\tsw $v0, {i.left.getSymbolEntry().getOffset()}($fp)')

		if isinstance(i,PrintAst):
			print(f'\tli $v0, 1')
			if isinstance(i.right,NameAst):
				print(f'\tlw $a0, {i.right.getSymbolEntry().getOffset()}($fp)')
			else:
				print(f'\tli $a0, {i.right.getNumber()}')

			print(f'\tsyscall')
			print(f'\tli $v0, 11')
			print(f'\tli $a0, 10')
			print(f'\tsyscall')

	print("# Epilogue Begins")
	print(f'epilogue_{function.getFunctionName()}:')
	print(f'\tadd $sp, $sp, {localSpaceRequired}')
	print(f'\tlw $fp, -4($sp)')
	print(f'\tlw $ra, 0($sp)')
	print(f'\tjr\t$ra')
	print('#Epilogue Ends')

