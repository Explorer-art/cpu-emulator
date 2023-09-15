#!usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

MAX_SIZE = 65535

points = [0] * MAX_SIZE # Points

memory = [0] * MAX_SIZE # Memory

stack = []

run = True

#====================================== Registers ======================================
IP = 0 # Instruction pointer
SP = 0

AX = 0
BX = 0
CX = 0
DX = 0

#====================================== Flags ======================================

PF = 0
ZF = 0
SF = 0

#====================================== Memory ======================================

def get_memory(address):
	global memory
	value = memory[address]
	return value

def set_memory(address, value):
	global memory
	memory[address] = value

#====================================== Stack ======================================

def PUSH(value):
	global stack, SP

	SP += 1

	stack.append(value)

def POP(dst):
	global stack, SP, AX, BX, CX, DX

	SP -= 1

	globals()[dst] = stack.pop()

#====================================== Output ======================================

def console(command, step):
	print(f"\nCommand: {command}")
	print(f"Step: {step}")
	print(f"IP: {IP}\n")
	print(f"AX = {AX}")
	print(f"BX = {BX}")
	print(f"CX = {CX}")
	print(f"DX = {DX}")
	print("")
	print(f"PF = {PF}    ZF = {ZF}    SF = {SF}\n")
	print("===================================================")

#====================================== Load ======================================

def load_source(filename):
	file = open(filename, "r")
	src = file.readlines()
	file.close()

	return src

def check_number_operand(value):
	for l in value:
		if l == "0":
			return True
		elif l == "1":
			return True
		elif l == "2":
			return True
		elif l == "3":
			return True
		elif l == "4":
			return True
		elif l == "5":
			return True
		elif l == "6":
			return True
		elif l == "7":
			return True
		elif l == "8":
			return True
		elif l == "9":
			return True

	return False

def translate(src):
	prg = [0] * MAX_SIZE

	i = -1

	b = -1

	point = False

	for line in src:
		i += 1
		if point == True:
			i -= 1
			point = False

		for l in line:
			if point == True:
				if points[b] == 0:
					points[b] = [l, i]
				else:
					point_data = points.pop(b)
					point_data = point_data[0]
					point_data += l
					points[b] = [point_data, i]

			if l == ":":
				point = True
				b += 1

	i = -1

	for line in src:
		i += 1

		if point == True:
			i -= 1
			point = False

		line_final = ""

		for l in line:
			if l == "#":
				break

			if l == ",":
				continue

			line_final += l

		line = line_final

		line = line.replace("\n", "")

		code = line.split(" ")

		opcode = code[0].lower()

		if len(code) > 2:
			if code[2] == "":
				pr = code[2]
				code.remove(pr)

		if len(code) == 1:
			if ":" in opcode:
				i -= 1
				continue

			prg[i] = [opcode, []]
		elif len(code) == 2:
			arg_1 = code[1]

			if check_number_operand(arg_1) == True:
				arg_1 = int(arg_1)

			if opcode == "jmp" or opcode == "loop" or opcode == "jle" or opcode == "je":
				for e in points:
					try:
						point_data_a = e[0].replace("\n", "")
						address = e[1]
						if point_data_a == arg_1:
							arg_1 = address
					except:
						continue

			prg[i] = [opcode, [arg_1]]
		elif len(code) == 3:
			arg_1 = code[1]

			if check_number_operand(arg_1) == True:
				arg_1 = int(arg_1)

			arg_2 = code[2]

			if check_number_operand(arg_2) == True:
				arg_2 = int(arg_2)

			prg[i] = [opcode, [arg_1, arg_2]]

	return prg

def decoder(prg):
	# for code in prg:
	# 	opcode = code[0].lower()
	# 	if opcode == "add":
	# 		code[0] = "add"
	pass

def load_code(prg):
	global memory

	i = -1

	for code in prg:
		i += 1
		memory[i] = code

#====================================== ALU  ======================================

def ADD(src):
	global AX, BX, CX, DX

	if type(src) is int:
		if src.bit_length() <= 16:
			AX = AX + src
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[src].bit_length() <= 16:
			AX = AX + globals()[src]
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def SUB(src):
	global AX, BX, CX, DX

	if type(src) is int:
		if src.bit_length() <= 16:
			AX = AX - src
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[src].bit_length() <= 16:
			AX = AX - globals()[src]
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def MUL(src):
	global AX, BX, CX, DX

	if type(src) is int:
		if src.bit_length() <= 16:
			AX = AX * src
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[src].bit_length() <= 16:
			AX = AX * globals()[src]
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def DIV(src):
	global AX, BX, CX, DX

	if type(src) is int:
		if src.bit_length() <= 16:
			AX = AX // src
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[src].bit_length() <= 16:
			AX = AX // globals()[src]
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def XOR(dst, src):
	global AX, BX, CX, DX

	if type(src) is int:
		if src.bit_lenght() <= 16:
			if globals()[dst] ^ src:
				globals()[dst] = 1
			else:
				globals()[dst] = 0
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[src].bit_length() <= 16:
			if globals()[dst] ^ globals()[src]:
				globals()[dst] = 1
			else:
				globals()[dst] = 0
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def INC(reg):
	global AX, BX, CX, DX

	globals()[reg] += 1

def DEC(reg):
	global AX, BX, CX, DX

	globals()[reg] -= 1

#====================================== CPU ======================================

def MOV(dst, src):
	global AX, BX, CX, DX

	if type(src) is int:
		if src.bit_length() <= 16:
			globals()[dst] = src
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[src].bit_length() <= 16:
			globals()[dst] = globals()[src]
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def LDA(address):
	global memory, AX

	if type(address) is int:
		if address.bit_length() <= 16:
			AX = get_memory(address)
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[address].bit_length() <= 16:
			AX = get_memory(globals()[address])
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def STA(address):
	global memory, AX

	if type(address) is int:
		if address.bit_length() <= 16:
			set_memory(address, AX)
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[address].bit_length() <= 16:
			set_memory(globals()[address], AX)
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def CMP(value_1, value_2):
	global AX, BX, CX, DX, ZF

	if type(value_1) is int and type(value_2) is int:
		if value_1.bit_length() <= 16 and value_2.bit_length() <= 16:
			if value_1 == value_2:
				ZF = 1
			else:
				ZF = 0
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()
	else:
		if globals()[value_1].bit_length() <= 16 and globals()[value_2].bit_length() <= 16:
			if globals()[value_1] == globals()[value_2]:
				ZF = 1
			else:
				ZF = 0
		else:
			print("Error! The number of bits is greater than 16.")
			sys.exit()

def JMP(address):
	global IP

	if address <= 65535:
		IP = address
	else:
		print("Error! The number of bits is greater than 16.")
		sys.exit()

def LOOP(address):
	global IP, CX

	if address <= 65535:
		if CX > 0 and CX <= 65535:
			IP = address
			DEC("CX")
	else:
		print("Error! The number of bits is greater than 16.")
		sys.exit()

def JE(address):
	global IP, ZF

	if address <= 65535:
		if ZF == 1:
			IP = address
	else:
		print("Error! The number of bits is greater than 16.")
		sys.exit()

def HLT():
	global run

	run = False

#====================================== Executor ======================================

def executor():
	global IP, memory, AX, BX, CX, DX

	step = 0

	while True:
		while run == True:
			step += 1

			code = memory[IP]

			if code == 0:
				continue
			else:
				opcode = code[0]

			if opcode == "add":
				src = code[1][0]

				ADD(src)
			elif opcode == "sub":
				src = code[1][0]

				SUB(src)
			elif opcode == "mul":
				src = code[1][0]

				MUL(src)
			elif opcode == "div":
				src = code[1][0]

				DIV(src)
			elif opcode == "xor":
				dst = code[1][0]
				src = code[1][1]

				XOR(dst, src)
			elif opcode == "inc":
				src = code[1][0]

				INC(src)
			elif opcode == "dec":
				src = code[1][0]

				DEC(src)
			elif opcode == "mov":
				dst = code[1][0]
				src = code[1][1]

				MOV(dst, src)
			elif opcode == "cmp":
				value_1 = code[1][0]
				value_2 = code[1][1]

				CMP(value_1, value_2)
			elif opcode == "lda":
				address = code[1][0]

				LDA(address)
			elif opcode == "sta":
				address = code[1][0]

				STA(address)
			elif opcode == "jmp":
				address = code[1][0]
				IP += 1
				JMP(address)
				console(code, step)
				continue
			elif opcode == "loop":
				address = code[1][0]
				IP += 1
				LOOP(address)
				console(code, step)
				continue
			elif opcode == "je":
				address = code[1][0]
				IP += 1
				JE(address)
				console(code, step)
				continue
			elif opcode == "push":
				value = code[1][0]

				PUSH(value)
			elif opcode == "pop":
				dst = code[1][0]

				POP(dst)
			elif opcode == "hlt":
				HLT()

			console(code, step)

			IP += 1

#====================================== Main ======================================

def main():
	if len(sys.argv) < 2:
		print("Error! The file is not defined.")
		sys.exit()

	filename = sys.argv[1]

	src = load_source(filename) # Загружаем код

	prg = translate(src) # Кодируем в опкоды и операнды

	load_code(prg) # Загружаем код в оперативную память

	print("CPU Emulator v1.0 by Truzme_\n")
	print("===================================================")

	executor() # Запускаем выполнение кода из оперативной памяти

#====================================== Start ======================================

if __name__ == "__main__":
	main()