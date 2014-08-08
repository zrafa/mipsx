



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

class Example(Frame):
  


     def __init__(self, parent):
      	Frame.__init__(self, parent)   
         
       	self.parent = parent
        
   #     self.initUI()
        
    #def initUI(self):
      
    	def prox_instruccion():
		p.stdin.write('next\n')
		mostrar_en(area4, "proximo")


		memoria()
		registros()
		estado()
		listado()

	def salida(w, findelinea):
		w.delete("1.0", END)
				
		a = p.stdout.readline()
#		while not "(gdb)" in a:
		while not findelinea in a:
			a = a.replace('(gdb) ', '')				
			w.insert(END,a)		
			a = p.stdout.readline() 		
		a = a.replace('(gdb) ', '')				
		w.insert(END,a)		
	
	def mostrar_en(w, findelinea):
#		salida(w)
		p.stdin.write(findelinea)
		p.stdin.write('\r\n')
		salida(w, findelinea)

	def mostrar_en_depuracion():
		
     		file = open("/tmp/archivotemp.txt")
	        contents = file.read()
		area4.delete('1.0',END)
		area4.insert('1.0',contents)
		file.close()

		

	def memoria():
#		p.stdin.write('x/15i $pc\n')
		p.stdin.write('x/40xw $pc\n')
		mostrar_en(area3, "memoria")
	

	def estado():
		p.stdin.write('info frame\n')
		mostrar_en(area4, "estado")


	def registros():
		p.stdin.write('info register\n')
		mostrar_en(area1, "registros")


	def listado():
		p.stdin.write('list 1,100\n')
		mostrar_en(area2, "listado")

	def compilarycargar():
		print self.archivoactual
		tub = Popen(['./compilarycargar.sh', self.archivoactual], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		mostrar_en_depuracion()
		if tub.returncode == 0:
			area4.insert(END, "Compilacion y carga : OK")

			# Abrimos con gdb el archivo ejecutable
			ejecutable = self.archivoactual+".elf"
			gdbfile = 'file '+ejecutable+' \n'
			p.stdin.write(gdbfile)
			# Respondemos "y"es a recargar			
			gdbfile = 'y '+ejecutable+' \n'
			p.stdin.write(gdbfile)

			# Nos conectamos al gdbserver
			ip_mips="10.0.15.232"
			comando='target remote '+ip_mips+':4567\n'
			p.stdin.write(comando)
			#'target remote 192.168.0.71:4567\n')
			mostrar_en(area4,"estado")
		else:
			area4.insert(END, "ERROR al compilar y cargar")
			mostrar_en_depuracion()

	def cargar():
			mostrar_en_depuracion()
#		else:
#			p.stdin.write('file a.out \n')
#			# Nos conectamos al gdbserver
#			p.stdin.write('target remote 192.168.0.71:4567\n')
#			mostrar_en(area4, "estado")


        self.parent.title("Mipsx - GUI for gdb multiarch anti spim :) ")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        lbl = Label(self, text="Registros                                      GDB en MIPS - MR3020")
        lbl.grid(row=1,column=2, sticky=W, pady=4, padx=5)
        

        area1 = Text(self,height=15,width=80)
        area1.grid(row=2, column=2, columnspan=1, rowspan=5, 
            sticky=E+W+S+N)
        
        lbl = Label(self, text="Programa en Assembler")
        lbl.grid(row=7, column=2, pady=1, padx=1, sticky=W+N+E+S)
        
    	area2 = Text(self, height=12,width=80)
        area2.grid(row=8, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Memoria")
        lbl.grid(row=13, column=2, pady=1, padx=1, sticky=W+N+E+S)

        area3 = Text(self,height=15,width=80)
        area3.grid(row=14, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl4 = Label(self, text="Mensajes de Depuracion")
        lbl4.grid(row=13, column=0, pady=1, padx=1, sticky=W+N+E+S)

        area4 = Text(self,height=8,width=80)
        area4.grid(row=14, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Editor del Programa")
        lbl.grid(row=1,column=0, sticky=W, pady=4, padx=5) 
     
	area5 = ScrolledText(self,height=29,width=80)
	area5.grid(row=2, column=0, columnspan=1, rowspan=10, 
            padx=1, sticky=E+W+S+N)

        abtn = Button(self, text="SALIR",command=salir)
        abtn.grid(row=2, column=1, padx=10, sticky=W)

        cbtn = Button(self, text="Run")
        cbtn.grid(row=3, column=1, padx=10, sticky=W)
        
        cbtn3 = Button(self, text="Next", command=prox_instruccion)
        cbtn3.grid(row=4, column=1, padx=10, sticky=W)
        
        cbtn4 = Button(self, text="Breakpoint")
        cbtn4.grid(row=5, column=1, padx=10, sticky=W)

        cbtn5 = Button(self, text="Compilar y Cargar", command=compilarycargar)
        cbtn5.grid(row=6, column=1, padx=10, sticky=W)

#        cbtn6 = Button(self, text="Cargar", command=cargar)
#        cbtn6.grid(row=6, column=1, padx=10, sticky=W)

	archivoactual = "hello.s"
	archivotemp = "/tmp/archivotemp.txt"
	ip_mips = "10.0.15.232"

	def abrir_en_editor(archivo):
		fd = open(archivo)      
		contents = fd.read()
		area5.delete('1.0',END)
	        area5.insert('1.0',contents)
	        fd.close()
	        self.archivoactual = archivo
		print self.archivoactual

	def open_command():
	        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
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
	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)
	menu.add_cascade(label="Archivo", menu=filemenu)
	filemenu.add_command(label="Nuevo", command=dummy)
	filemenu.add_command(label="Abrir...", command=open_command)
	filemenu.add_command(label="Guardar...", command=save_command)
	filemenu.add_separator()
	filemenu.add_command(label="Salir", command=salir)
	helpmenu = Menu(menu)
	menu.add_cascade(label="Ayuda", menu=helpmenu)
	helpmenu.add_command(label="Acerca de...", command=about_command)
 	abrir_en_editor("hello.s")
        


def salir():
	clave = "root"
	comando = "killall gdbserver"
	ip_mips = "10.0.15.232"
	killgdbserver = Popen(['sshpass', '-p', clave, 'ssh', '-o', 'StrictHostKeyChecking=no', '-l', 'root', ip_mips, comando], stdout=PIPE, stdin=PIPE, stderr=STDOUT)	
	quit()



# Para el editor
def abrirarchivo():

        file = askopenfilename(parent=root)
        if file != None:
	        f = open(file, "r")
	        contents = f.read()
        
		# contents = file.read()
		app.mostrar_en_editor(contents)
#		app.area5.delete("1.0", END)
#		app.area5.insert('1.0',contents)
		f.close()	
 
def guardararchivo(self):
    file = tkFileDialog.asksaveasfile(mode='w')
    if file != None:
    # slice off the last character from get, as an extra return is added
        data = app.area5.get('1.0', END+'-1c')
        file.write(data)
        file.close()

def nuevoarchivo():
    print "I am a Dummy Command, I will be removed in the next step"         
 
def acercade():
    label = tkMessageBox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")


def main():
  
   	
#    	app = Example(root)
    
	# Para el menu FILE
	
#	menubar = Menu(root)
#	filemenu = Menu(menubar, tearoff=0)
#	filemenu.add_command(label="Nuevo", command=nuevoarchivo)
#	filemenu.add_separator()
#	filemenu.add_command(label="Acerca de", command=acercade)
#	filemenu.add_separator()
#	filemenu.add_command(label="Salir", command=root.quit)

#	menubar.add_cascade(label="Archivo", menu=filemenu)
#	root.config(menu=menubar)

	root.mainloop()  




def openfile():

	filename = askopenfilename(parent=root)

	clave="root"
	archivo = ntpath.basename(filename)	# Quitamos la ruta y nos quedamos con el nombre del archivo

	copiar = Popen(['sshpass', '-p', clave, 'scp', filename, 'root@192.168.0.71:/tmp'])
	copiar.wait()

	# Abrimos con gdb el archivo ejecutable	
	gdbfile = 'file '+filename+' \n'
	p.stdin.write(gdbfile)

	# Nos conectamos al gdbserver
	p.stdin.write('target remote 192.168.0.71:4567\n')

	# Iniciamos en el host remoto el gdbserver
	comando = "gdbserver 0.0.0.0:4567 /tmp/"+archivo
	gdbserver = Popen(['sshpass', '-p', clave, 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@192.168.0.71', comando], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	app.mostrar_en(app.area4,"estado")
#	salida(area4)

if __name__ == '__main__':
	p = Popen(['gdb-multiarch'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	root = Tk()    

    	app = Example(root)
	main()  






