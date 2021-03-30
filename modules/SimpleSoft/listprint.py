#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import subprocess

class objImpresoras():
	def __init__(self):
		self.lista=[]
		if  os.name == 'nt': #Windows
			import win32print	
			for i in range (1,6):
				for p in win32print.EnumPrinters(i):
					if  not (p[2] in self.lista):
						self.lista.append (p[2])

		else: #linux
			p = subprocess.Popen(["lpstat", "-a"], stdout=subprocess.PIPE)
			output, err = p.communicate()
			#print (output)
			output = output.split(b'\n')
			for p in output:
				p=p.split(b' ')
				if len (p[0].strip())>0:
					self.lista.append (p[0])
			print (self.lista)
	
	def getLista(self):
		return self.lista

if __name__ == "__main__":
	obj=objImpresoras()
	print (obj.getLista())

	#1:49 archivo de imagen