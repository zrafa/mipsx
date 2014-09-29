#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original del ejemplo de una aplicacion Tk: Jan Bodnar
last modified: December 2010
website: www.zetcode.com

Modificado y ampliado para ser una GUI de GDB para MIPS. 
(C) 2014 - Rafael Ignacio Zurita <rafa@fi.uncoma.edu.ar>

Lea el archivo README.md para conocer la licencia de este programa.
"""

import time
import sys
import random

from subprocess import Popen, PIPE, STDOUT

from Tkinter import *
from ttk import Frame, Button, Label, Style

# Para extrar el nombre de archivo sin ruta
import ntpath

from ScrolledText import *
import tkFileDialog
import tkMessageBox

class MipsxTkGui(Frame):
  


    def __init__(self, parent, control):

      	Frame.__init__(self, parent)   
         
       	self.parent = parent

        self.parent.title("Mipsx - GUI for gdb multiarch")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

	# Para expandir cuando las ventanas cambian de tamao 
	for i in range(3):
		self.columnconfigure(i, weight=1)
	for i in range(20):
		self.rowconfigure(i, weight=1)

        lbl = Label(self, text="Registros")
        lbl.grid(row=1,column=2, sticky=W, pady=4, padx=5)
        

        self.registros = Text(self,height=12,width=80)
        self.registros.grid(row=2, column=2, columnspan=1, rowspan=5, 
            sticky=E+W+S+N)
        
        lbl = Label(self, text="Programa en Assembler y Prorama Binario Decodificado (disassemble) ")
        lbl.grid(row=7, column=2, pady=1, padx=1, sticky=W+N+E+S)
        
    	self.programa = Text(self, height=6,width=80)
        self.programa.grid(row=8, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text='Memoria - Segmento de datos (debe existir la etiqueta "memoria") - Segmento de texto - Pila')
        lbl.grid(row=13, column=2, pady=1, padx=1, sticky=W+N+E+S)

        self.memoria = Text(self,height=15,width=80)
        self.memoria.grid(row=14, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl4 = Label(self, text="Mensajes de Depuracion")
        lbl4.grid(row=13, column=0, pady=1, padx=1, sticky=W+N+E+S)

        self.mensajes = Text(self,height=8,width=60)
        self.mensajes.grid(row=14, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Editor del Programa")
        lbl.grid(row=1,column=0, sticky=W, pady=4, padx=5) 
     
	self.editor = ScrolledText(self,height=20,width=60)
	self.editor.grid(row=2, column=0, columnspan=1, rowspan=10, 
            padx=1, sticky=E+W+S+N)
        
      
	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)

	menu.add_cascade(label="Archivo", menu=filemenu)
	filemenu.add_command(label="Nuevo", command=control.nuevo)
	filemenu.add_command(label="Abrir...", command=control.abrir)
	filemenu.add_command(label="Guardar...", command=control.guardar)
	filemenu.add_separator()
	filemenu.add_command(label="Salir", command=control.salir)


	menu.add_command(label="Run", command=control.ejecutar)
	menu.add_command(label="Next", command=control.prox_instruccion)
	menu.add_command(label="Breakpoint", command=control.no_hacer_nada)
	menu.add_command(label="Compilar y Cargar", command=control.compilarycargar)

	helpmenu = Menu(menu)
	menu.add_cascade(label="Ayuda", menu=helpmenu)
	helpmenu.add_command(label="Acerca de...", command=control.acercade)
	menu.add_command(label="Salir", command=control.salir)

    def limpiar_panel(self, panel):
		panel.delete('1.0',END)

    def panel_agregar(self, panel, contenido):
		panel.insert(END, contenido)

    def panel_leer(self, panel):
		return panel.get('1.0', END+'-1c')

    def mostrar_en_area(self, area):
		area.insert(END,contents)

    # Al abrir un archivo deseamos tener un area de trabajo cero
    def limpiar_paneles(self):
		self.mensajes.delete('1.0',END)
		self.memoria.delete('1.0',END)
		self.programa.delete('1.0',END)
		self.registros.delete('1.0',END)



class MipsxControl(Frame):


    def __init__(self, parent):

    	self.paneles = MipsxTkGui(parent, self)

	self.ejecucion = False

	# PUERTOyPS es usado para generar archivos temporales y puerto de conexion
	self.PUERTOyPS = str( random.randrange(4000,8000+1) )

	# Variables globales 
	self.archivoactual = "hello.s"
	self.archivoacompilar = "hello.s"
	self.archivotemp = "/tmp/archivotemp"+self.PUERTOyPS+".txt"
	# ip_mips = "10.0.15.232"
	self.ip_mips = "10.0.15.50"
	# ip_mips = "192.168.0.71"

	# Abrimos el archivo base
 	self.abrir_en_editor("hello.s")
	
	# Si se finaliza el programa con click en el boton X llamamos a salir
	root.protocol("WM_DELETE_WINDOW", self.salir)


    def prox_instruccion(self):

		gdb.stdin.write('next\n')
		self.mostrar_en(self.paneles.mensajes, "proximo")

		self.estado()
		if self.ejecucion:
			self.memoria()
			self.registros()
			self.listado()
		
    def ejecutar(self):
		while self.ejecucion:
			self.prox_instruccion()

    def salida(self, w, findelinea):
		self.paneles.limpiar_panel(w)
				
		a = gdb.stdout.readline()
		while not findelinea in a:
			# Esto es para saber si la ejecucion termino'. 
			# TODO: Hay que quitarlo de este metodo. Donde ponerlo?
			if "No stack" in a:
				self.ejecucion = False
				# w.insert(END,'\n\nEjecucion FINALIZADA\n\n')
				self.paneles.panel_agregar(w,'\n\nEjecucion FINALIZADA\n\n')

			a = a.replace('(gdb) ', '')				
			# w.insert(END,a)		
			self.paneles.panel_agregar(w, a)
			a = gdb.stdout.readline() 		
	
    def mostrar_en(self, w, findelinea):
		gdb.stdin.write(findelinea)
		gdb.stdin.write('\r\n')
		self.salida(w, findelinea)

    def mostrar_en_depuracion(self):
		
     		file = open("/tmp/archivotemp"+self.PUERTOyPS+".txt")
	        contents = file.read()
		file.close()

		self.paneles.panel_agregar(self.paneles.mensajes, contents)

		

    def memoria(self):
		# Para mostrar el segmento de datos, la etiqueta memoria debe estar al principio
		gdb.stdin.write('info address memoria\n')
		gdb.stdin.write('infomemoria\n')
		a = gdb.stdout.readline()
		solicitar_seg_de_datos = ""
		while not "infomemoria" in a:
			print "a : "+a
			if "Symbol " in a:
				a = a.replace('(gdb) Symbol "memoria" is at ', '')
				a = a.replace(' in a file compiled without debugging.','')
				solicitar_seg_de_datos = "x/40xw "+a+"\n"
			a = gdb.stdout.readline()
			
		if solicitar_seg_de_datos == "":
			gdb.stdin.write('x/40xw $pc\n')
		else:
			gdb.stdin.write(solicitar_seg_de_datos)
		gdb.stdin.write('x/50xw main\n')
		gdb.stdin.write('x/40xw $sp\n')
		self.mostrar_en(self.paneles.memoria, "memoria")
	

    def estado(self):
		gdb.stdin.write('info frame\n')
		self.mostrar_en(self.paneles.mensajes, "estado")
     		file = open("/tmp/archivotemp"+self.PUERTOyPS+".txt")
	        contents = file.readline()
		while not "Remote" in contents:
			print contents
			self.paneles.panel_agregar(self.paneles.mensajes, contents)
	        	contents = file.readline()

		self.paneles.panel_agregar(self.paneles.mensajes, "----------------------------------------\nSalida Estandar : \n\n")

		contents = file.read()
		file.close()
		self.paneles.panel_agregar(self.paneles.mensajes, contents) 


    def registros(self):
		gdb.stdin.write('info register\n')
		self.mostrar_en(self.paneles.registros, "registros")


    def listado(self):
		gdb.stdin.write('list 1,100\n')
		# gdb.stdin.write('disas main\n')
		gdb.stdin.write('disas \n')
		self.mostrar_en(self.paneles.programa, "listado")

    def compilarycargar(self):
		self.paneles.limpiar_panel(self.paneles.mensajes)
		self.paneles.panel_agregar(self.paneles.mensajes, "Compilando y Cargando ...\r\n")
		root.update_idletasks()

		# Nos liberamos del debugging actual
		gdb.stdin.write('detach \n')
		self.guardar_archivo_a_compilar()
		tub = Popen(['mipsx_compilarycargar.sh', self.archivoacompilar, self.PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		self.mostrar_en_depuracion()

		# Si la compilacion y carga no tuvo errores
		if tub.returncode == 0:
			self.paneles.panel_agregar(self.paneles.mensajes, "Compilacion y Carga OK\r\n")


			ejecutable = self.archivoacompilar+".elf"
			ejecutable = ntpath.basename(ejecutable)

			# Nos conectamos al gdbserver
			# ip_mips="10.0.15.232"
			# ip_mips="192.168.0.71"

			ip_mips="10.0.15.50"
			comando='target remote '+ip_mips+':'+self.PUERTOyPS+'\n'
			gdb.stdin.write(comando)

			# Respondemos "y"es a recargar			
			gdb.stdin.write('y \n')

			# Abrimos con gdb el archivo ejecutable
			gdbfile = 'file /tmp/'+ejecutable+'\n'
			gdb.stdin.write(gdbfile)
			# Respondemos "y"es a recargar			
			gdb.stdin.write('y \n')
		
			gdb.stdin.write('delete \n')
			gdb.stdin.write('y \n')
			gdb.stdin.write('break main\n')
			gdb.stdin.write('continue\n')
			self.ejecucion = True

			self.mostrar_en(self.paneles.mensajes,"estado")
			self.memoria()
			self.registros()
			self.listado()
		else:
			self.paneles.panel_agregar(self.paneles.mensajes, "ERROR al compilar y cargar") 
			mostrar_en_depuracion()


    def abrir_en_editor(self, archivo):

		fd = open(archivo)      
		contents = fd.read()
	        fd.close()

		self.paneles.limpiar_panel(self.paneles.editor)
		self.paneles.panel_agregar(self.paneles.editor, contents)
	        self.archivoactual = archivo

    def abrir(self):
		FILEOPENOPTIONS = dict(defaultextension='*.s',
                  filetypes=[('Archivo assembler','*.s'), ('Todos los archivos','*.*')])
	        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file',
				**FILEOPENOPTIONS)
	        if file != None:
			self.paneles.limpiar_paneles()
			self.abrir_en_editor(file.name)	      
 
    def guardar_archivo_a_compilar(self):
		self.archivoacompilar = "/tmp/archivo"+self.PUERTOyPS+".s"
		tub = Popen(['rm', self.archivoacompilar], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		tub = Popen(['touch', self.archivoacompilar], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		tmp = open(self.archivoacompilar, "w")
	    	if tmp != None:
	        	# data = editor.get('1.0', END+'-1c')
	        	data = self.paneles.panel_leer(self.paneles.editor)
	        	tmp.write(data)
	        	tmp.close()

			archivotmppwd = "archivo"+self.PUERTOyPS+".s"
			tub = Popen(['cp', self.archivoacompilar, archivotmppwd], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
			streamdata = tub.communicate()[0]
	

    def guardar(self):
	    file = tkFileDialog.asksaveasfile(mode='w')
	    if file != None:
	    # slice off the last character from get, as an extra return is added
	        # data = editor.get('1.0', END+'-1c')
	        data = self.paneles.panel_leer(self.paneles.editor)
	        file.write(data)
	        file.close()
		self.archivoactual = file.name
                print self.archivoactual
         
    def exit_command(self):
	    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
	        root.destroy()
	 
    def acercade(self):
	    label = tkMessageBox.showinfo("Acerca de", "MIPSX - GUI for gdb multiarch\n\nEntorno de desarrollo en lenguaje assembler arquitectura MIPS\nEste programa ensabla, genera el programa ejecutable, y lo ejecuta en modo debug en una maquina MIPS real\n\nCopyright 2014 Rafael Ignacio Zurita\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")
		         
 
    def nuevo(self):
		self.paneles.limpiar_panel(self.paneles.editor)

    def no_hacer_nada(self):
		print "nada por hacer"

    def archivo_sin_guardar(self):

		data = self.paneles.panel_leer(self.paneles.editor)

		fd = open(self.archivoactual)      
		contents = fd.read()
	        fd.close()

		if data == contents:
			return False

		res = tkMessageBox.askquestion("Confirmar", "Archivo sin guardar\nEsta seguro de finalizar el programa?", icon='warning')
		if res == 'yes':
			return False

		return True

    def salir(self):
		if self.archivo_sin_guardar():
			return

#		ip_mips = "10.0.15.50"
#		tub = Popen(['mipsx_finalizar_gdbserver.sh', ip_mips, self.PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#		streamdata = tub.communicate()[0]

		# Borrar todos los temporales
		tmp = "/tmp/archivo"+self.PUERTOyPS+".s"
		tmp2 = "archivo"+self.PUERTOyPS+".s"
		tmp3 = "/tmp/archivo"+self.PUERTOyPS+".s.elf"
		tmp4 = "/tmp/archivotemp"+self.PUERTOyPS+".txt"
		tub = Popen(['rm', tmp, tmp2, tmp3, tmp4], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]


                tmp2 = "/tmp/archivo"+PUERTOyPS+".s.o"
                ip_mips = "10.0.15.50"
                tub = Popen(['mipsx_finalizar_gdbserver.sh', ip_mips, PUERTOyPS, tmp, tmp2, tmp3, tmp4], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]

		quit()


        


 
 

def main():
  
	root.mainloop()  



if __name__ == '__main__':
	gdb = Popen(['gdb-multiarch'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	root = Tk()    

	# Para expandir cuando las ventanas cambian de tamao 
	root.columnconfigure(0,weight=1)
	root.rowconfigure(0, weight=1)

    	app = MipsxControl(root)
	main()  






