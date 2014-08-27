

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original del ejemplo de una aplicacion Tk: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
Modificado y ampliado para ser una GUI de GDB para MIPS. Por Rafael Ignacio Zurita
"""

import time
import sys
import random

from subprocess import Popen, PIPE, STDOUT

#from Tkinter import Tk, Text, BOTH, W, N, E, S
from Tkinter import *
from ttk import Frame, Button, Label, Style

# Para el menu FILE
#from tkFileDialog import askopenfilename

# Para extrar el nombre de archivo sin ruta
import ntpath

from ScrolledText import *
import tkFileDialog
import tkMessageBox

class Mipsx(Frame):
  


     def __init__(self, parent):
      	Frame.__init__(self, parent)   
         
       	self.parent = parent
        
   #     self.initUI()
        
    #def initUI(self):
      
	self.ejecucion = False
    	def prox_instruccion():
		if self.ejecucion == False:
			p.stdin.write('run\n')
			self.ejecucion = True
		else:
			p.stdin.write('next\n')

		mostrar_en(area4, "proximo")


		finalizado=estado()
		if not finalizado:
			memoria()
			registros()
			listado()

	def salida(w, findelinea):
		w.delete("1.0", END)
				
		a = p.stdout.readline()
#		while not "(gdb)" in a:
		while not findelinea in a:
			a = a.replace('(gdb) ', '')				
			w.insert(END,a)		
			a = p.stdout.readline() 		
		# a = a.replace('(gdb) ', '')				
		# w.insert(END,a)		
	
	def mostrar_en(w, findelinea):
#		salida(w)
		p.stdin.write(findelinea)
		p.stdin.write('\r\n')
		salida(w, findelinea)

	def mostrar_en_depuracion():
		
     		file = open("/tmp/archivotemp.txt")
	        contents = file.read()
		#area4.delete('1.0',END)
		area4.insert(END,contents)
		file.close()

		

	def memoria():
#		p.stdin.write('x/15i $pc\n')
		p.stdin.write('x/40xw $pc\n')
		mostrar_en(area3, "memoria")
	

	def estado():
		p.stdin.write('info frame\n')
		mostrar_en(area4, "estado")
     		file = open("/tmp/archivotemp.txt")
	        contents = file.readline()
		finalizado=False
		while not "Remote" in contents:
			if "No stack" in contents:
				print "FINALIZADO"
				finalizado=True
			else:
				print contents
			area4.insert(END,contents)
	        	contents = file.readline()
		contents = file.readline()
		file.close()

		area4.insert(END,"----------------------------------------\nSalida Estandar : \n")
		area4.insert(END,contents)
		return finalizado


	def registros():
		p.stdin.write('info register\n')
		mostrar_en(area1, "registros")


	def listado():
		p.stdin.write('list 1,100\n')
		mostrar_en(area2, "listado")

	def compilarycargar():
		area4.delete('1.0',END)
		area4.insert('1.0',"Compilando y Cargando ...\r\n")
		root.update_idletasks()
		print self.archivoactual+PUERTOyPS
#		tub = Popen(['./matargdbserver.sh', PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#		streamdata = tub.communicate()[0]
#		time.sleep(10);
		p.stdin.write('detach \n')
		comando='target disconnect\n'
		p.stdin.write(comando)

		tub = Popen(['./compilarycargar.sh', self.archivoactual], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		mostrar_en_depuracion()
		if tub.returncode == 0:
			area4.insert(END, "Compilacion y carga : OK\n")


			ejecutable = self.archivoactual+".elf"
			ejecutable = ntpath.basename(ejecutable)

			# Nos conectamos al gdbserver
			# ip_mips="10.0.15.232"
			# ip_mips="192.168.0.71"

			ip_mips="10.0.15.50"
			# comando='target extended-remote '+ip_mips+':4567\n'
			comando='target extended-remote '+ip_mips+':4567\n'
			p.stdin.write(comando)

			gdbfile = 'set remote exec-file /tmp/'+ejecutable+'\n'
			p.stdin.write(gdbfile)
			# Respondemos "y"es a recargar			
			p.stdin.write('y \n')

			# Abrimos con gdb el archivo ejecutable
			gdbfile = 'file /tmp/'+ejecutable+'\n'
			p.stdin.write(gdbfile)
			# Respondemos "y"es a recargar			
			#gdbfile = 'y '+ejecutable+' \n'
			p.stdin.write('y \n')
		
			p.stdin.write('delete \n')
			p.stdin.write('y \n')
			p.stdin.write('break main\n')
			self.ejecucion = False

			mostrar_en(area4,"estado")
		else:
			area4.insert(END, "ERROR al compilar y cargar")
			mostrar_en_depuracion()


	# PUERTOyPS=random.randrange(4000,5000+1)
	PUERTOyPS="4567"


        self.parent.title("Mipsx - GUI for gdb multiarch anti spim :) ")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

	# Para expandir cuando las ventanas cambian de tamao 
	for i in range(3):
		self.columnconfigure(i, weight=1)
	for i in range(20):
		self.rowconfigure(i, weight=1)

        lbl = Label(self, text="Registros                                      GDB en MIPS - MR3020")
        lbl.grid(row=1,column=2, sticky=W, pady=4, padx=5)
        

        area1 = Text(self,height=12,width=80)
        area1.grid(row=2, column=2, columnspan=1, rowspan=5, 
            sticky=E+W+S+N)
        
        lbl = Label(self, text="Programa en Assembler")
        lbl.grid(row=7, column=2, pady=1, padx=1, sticky=W+N+E+S)
        
    	area2 = Text(self, height=6,width=80)
        area2.grid(row=8, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Memoria")
        lbl.grid(row=13, column=2, pady=1, padx=1, sticky=W+N+E+S)

        area3 = Text(self,height=15,width=80)
        area3.grid(row=14, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl4 = Label(self, text="Mensajes de Depuracion")
        lbl4.grid(row=13, column=0, pady=1, padx=1, sticky=W+N+E+S)

        area4 = Text(self,height=8,width=60)
        area4.grid(row=14, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Editor del Programa")
        lbl.grid(row=1,column=0, sticky=W, pady=4, padx=5) 
     
	area5 = ScrolledText(self,height=20,width=60)
	area5.grid(row=2, column=0, columnspan=1, rowspan=10, 
            padx=1, sticky=E+W+S+N)


	archivoactual = "hello.s"
	archivotemp = "/tmp/archivotemp.txt"
	# ip_mips = "10.0.15.232"
	ip_mips = "10.0.15.50"
	# ip_mips = "192.168.0.71"

	def abrir_en_editor(archivo):
		fd = open(archivo)      
		contents = fd.read()
		area5.delete('1.0',END)
	        area5.insert('1.0',contents)
	        fd.close()
	        self.archivoactual = archivo
		print self.archivoactual

	def open_command():
		FILEOPENOPTIONS = dict(defaultextension='*.s',
                  filetypes=[('Archivo assembler','*.s'), ('Todos los archivos','*.*')])
	        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file',
				**FILEOPENOPTIONS)
	        if file != None:
			abrir_en_editor(file.name)	      
#		    contents = file.read()
#		    area5.delete('1.0',END)
#	            area5.insert('1.0',contents)
#	            file.close()
#	            self.archivoactual = file.name
#		    print self.archivoactual
 
	def save_command():
	    file = tkFileDialog.asksaveasfile(mode='w')
	    if file != None:
	    # slice off the last character from get, as an extra return is added
	        data = area5.get('1.0', END+'-1c')
	        file.write(data)
	        file.close()
		self.archivoactual = file.name
                print self.archivoactual
         
	def exit_command():
	    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
	        root.destroy()
	 
	def about_command():
	    label = tkMessageBox.showinfo("Acerca de", "MIPSX - GUI for gdb multiarch anti spim :)\n\nEntorno de desarrollo en lenguaje assembler arquitectura MIPS\nEste programa ensabla, genera el programa ejecutable, y lo ejecuta en modo debug en una maquina MIPS real\n\nCopyright 2014 Rafael Ignacio Zurita\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")
		         
 
	def dummy():
	    print "I am a Dummy Command, I will be removed in the next step"

	def salir():
		clave = "root"
		comando = "killall gdbserver"
		# ip_mips = "10.0.15.232"
		ip_mips = "10.0.15.50"
		# ip_mips = "192.168.0.71"
		killgdbserver = Popen(['sshpass', '-p', clave, 'ssh', '-o', 'StrictHostKeyChecking=no', '-l', 'root', ip_mips, comando], stdout=PIPE, stdin=PIPE, stderr=STDOUT)	
		quit()



	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)
	menu.add_cascade(label="Archivo", menu=filemenu)
	filemenu.add_command(label="Nuevo", command=dummy)
	filemenu.add_command(label="Abrir...", command=open_command)
	filemenu.add_command(label="Guardar...", command=save_command)
	filemenu.add_separator()
	filemenu.add_command(label="Salir", command=salir)


	menu.add_command(label="Run", command=salir)
	menu.add_command(label="Next", command=prox_instruccion)
	menu.add_command(label="Breakpoint", command=salir)
	menu.add_command(label="Compilar y Cargar", command=compilarycargar)

	helpmenu = Menu(menu)
	menu.add_cascade(label="Ayuda", menu=helpmenu)
	helpmenu.add_command(label="Acerca de...", command=about_command)
	menu.add_command(label="Salir", command=salir)
 	abrir_en_editor("hello.s")
        


 
 

def main():
  
	root.mainloop()  





if __name__ == '__main__':
	p = Popen(['gdb-multiarch'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	root = Tk()    

	# Para expandir cuando las ventanas cambian de tamao 
	root.columnconfigure(0,weight=1)
	root.rowconfigure(0, weight=1)

    	app = Mipsx(root)
	main()  






