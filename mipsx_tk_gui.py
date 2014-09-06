#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original del ejemplo de una aplicacion Tk: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
Modificado y ampliado para ser una GUI de GDB para MIPS. 
(C) 2014 - Rafael Ignacio Zurita <rafa@fi.uncoma.edu.ar>
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

        lbl = Label(self, text="Registros                                      GDB en MIPS - MR3020")
        lbl.grid(row=1,column=2, sticky=W, pady=4, padx=5)
        

        self.area1 = Text(self,height=12,width=80)
        self.area1.grid(row=2, column=2, columnspan=1, rowspan=5, 
            sticky=E+W+S+N)
        
        lbl = Label(self, text="Programa en Assembler y Prorama Binario Decodificado")
        lbl.grid(row=7, column=2, pady=1, padx=1, sticky=W+N+E+S)
        
    	self.area2 = Text(self, height=6,width=80)
        self.area2.grid(row=8, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text='Memoria - Segmento de datos (debe existir la etiqueta "memoria") - Segmento de texto - Pila')
        lbl.grid(row=13, column=2, pady=1, padx=1, sticky=W+N+E+S)

        self.area3 = Text(self,height=15,width=80)
        self.area3.grid(row=14, column=2, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl4 = Label(self, text="Mensajes de Depuracion")
        lbl4.grid(row=13, column=0, pady=1, padx=1, sticky=W+N+E+S)

        self.area4 = Text(self,height=8,width=60)
        self.area4.grid(row=14, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Editor del Programa")
        lbl.grid(row=1,column=0, sticky=W, pady=4, padx=5) 
     
	self.area5 = ScrolledText(self,height=20,width=60)
	self.area5.grid(row=2, column=0, columnspan=1, rowspan=10, 
            padx=1, sticky=E+W+S+N)
        
      
	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)

	menu.add_cascade(label="Archivo", menu=filemenu)
	filemenu.add_command(label="Nuevo", command=control.dummy)
	filemenu.add_command(label="Abrir...", command=control.open_command)
	filemenu.add_command(label="Guardar...", command=control.save_command)
	filemenu.add_separator()
	filemenu.add_command(label="Salir", command=control.salir)


	menu.add_command(label="Run", command=control.ejecutar)
	menu.add_command(label="Next", command=control.prox_instruccion)
	menu.add_command(label="Breakpoint", command=control.no_hacer_nada)
	menu.add_command(label="Compilar y Cargar", command=control.compilarycargar)

	helpmenu = Menu(menu)
	menu.add_cascade(label="Ayuda", menu=helpmenu)
	helpmenu.add_command(label="Acerca de...", command=control.about_command)
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
    def limpiar_areas(self):
		area4.delete('1.0',END)
		area3.delete('1.0',END)
		area2.delete('1.0',END)
		area1.delete('1.0',END)



class MipsxControl(Frame):


    def __init__(self, parent):

    	self.paneles = MipsxTkGui(parent, self)

	self.ejecucion = False
	self.PUERTOyPS = str( random.randrange(4000,5000+1) )

	# Variables globales 
	self.archivoactual = "hello.s"
	self.archivoacompilar = "hello.s"
	self.archivotemp = "/tmp/archivotemp"+self.PUERTOyPS+".txt"
	# ip_mips = "10.0.15.232"
	self.ip_mips = "10.0.15.50"
	# ip_mips = "192.168.0.71"



 	self.abrir_en_editor("hello.s")

	
	root.protocol("WM_DELETE_WINDOW", self.salir)


    def prox_instruccion(self):
		p.stdin.write('next\n')

		self.mostrar_en(self.paneles.area4, "proximo")

		self.estado()
		if self.ejecucion:
			self.memoria()
			self.registros()
			self.listado()
		
    def ejecutar(self):
		while self.ejecucion:
			prox_instruccion()

    def salida(self, w, findelinea):
		# w.delete("1.0", END)
		self.paneles.limpiar_panel(w)
				
		a = p.stdout.readline()
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
			a = p.stdout.readline() 		
	
    def mostrar_en(self, w, findelinea):
		p.stdin.write(findelinea)
		p.stdin.write('\r\n')
		self.salida(w, findelinea)

    def mostrar_en_depuracion(self):
		
     		file = open("/tmp/archivotemp"+self.PUERTOyPS+".txt")
	        contents = file.read()
		# area4.insert(END,contents)
		self.paneles.panel_agregar(self.paneles.area4, contents)
		file.close()

		

    def memoria(self):
		# Para mostrar el segmento de datos, la etiqueta memoria debe estar al principio
		p.stdin.write('info address memoria\n')
		p.stdin.write('infomemoria\n')
		a = p.stdout.readline()
		solicitar_seg_de_datos = ""
		while not "infomemoria" in a:
			print "a : "+a
			if "Symbol " in a:
				a = a.replace('(gdb) Symbol "memoria" is at ', '')
				a = a.replace(' in a file compiled without debugging.','')
				solicitar_seg_de_datos = "x/40xw "+a+"\n"
			a = p.stdout.readline()
			
		if solicitar_seg_de_datos == "":
			p.stdin.write('x/40xw $pc\n')
		else:
			p.stdin.write(solicitar_seg_de_datos)
		p.stdin.write('x/50xw main\n')
		p.stdin.write('x/40xw $sp\n')
		self.mostrar_en(self.paneles.area3, "memoria")
	

    def estado(self):
		p.stdin.write('info frame\n')
		self.mostrar_en(self.paneles.area4, "estado")
     		file = open("/tmp/archivotemp"+self.PUERTOyPS+".txt")
	        contents = file.readline()
		while not "Remote" in contents:
			print contents
			self.paneles.panel_agregar(self.paneles.area4, contents)
	        	contents = file.readline()

		self.paneles.panel_agregar(self.paneles.area4, "----------------------------------------\nSalida Estandar : \n\n")

		contents = file.read()
		file.close()
		self.paneles.panel_agregar(self.paneles.area4, contents) 
		# area4.insert(END,contents)


    def registros(self):
		p.stdin.write('info register\n')
		p.stdin.write('disas main\n')
		self.mostrar_en(self.paneles.area1, "registros")


    def listado(self):
		p.stdin.write('list 1,100\n')
		self.mostrar_en(self.paneles.area2, "listado")

    def compilarycargar(self):
		# area4.delete('1.0',END)
		self.paneles.limpiar_panel(self.paneles.area4)
		# area4.insert('1.0',"Compilando y Cargando ...\r\n")
		self.paneles.panel_agregar(self.paneles.area4, "Compilando y Cargando ...\r\n")
		root.update_idletasks()

		p.stdin.write('detach \n')
		self.guardar_archivo_a_compilar()
		tub = Popen(['mipsx_compilarycargar.sh', self.archivoacompilar, self.PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		self.mostrar_en_depuracion()

		if tub.returncode == 0:
			# area4.insert(END, "Compilacion y carga : OK\n")
			self.paneles.panel_agregar(self.paneles.area4, "Compilacion y Carga OK\r\n")


			ejecutable = self.archivoacompilar+".elf"
			ejecutable = ntpath.basename(ejecutable)

			# Nos conectamos al gdbserver
			# ip_mips="10.0.15.232"
			# ip_mips="192.168.0.71"

			ip_mips="10.0.15.50"
			comando='target remote '+ip_mips+':'+self.PUERTOyPS+'\n'
			p.stdin.write(comando)

			# Respondemos "y"es a recargar			
			p.stdin.write('y \n')

			# Abrimos con gdb el archivo ejecutable
			gdbfile = 'file /tmp/'+ejecutable+'\n'
			p.stdin.write(gdbfile)
			# Respondemos "y"es a recargar			
			p.stdin.write('y \n')
		
			p.stdin.write('delete \n')
			p.stdin.write('y \n')
			p.stdin.write('break main\n')
			p.stdin.write('continue\n')
			self.ejecucion = True

			self.mostrar_en(self.paneles.area4,"estado")
			self.memoria()
			self.registros()
			self.listado()
		else:
			# area4.insert(END, "ERROR al compilar y cargar")
			self.paneles.panel_agregar(self.paneles.area4, "ERROR al compilar y cargar") 
			mostrar_en_depuracion()


    def abrir_en_editor(self, archivo):
		fd = open(archivo)      
		contents = fd.read()
		# area5.delete('1.0',END)
		self.paneles.limpiar_panel(self.paneles.area5)
	        #area5.insert('1.0',contents)
		self.paneles.panel_agregar(self.paneles.area5, contents)

	        fd.close()
	        self.archivoactual = archivo
		print self.archivoactual

    def open_command(self):
		FILEOPENOPTIONS = dict(defaultextension='*.s',
                  filetypes=[('Archivo assembler','*.s'), ('Todos los archivos','*.*')])
	        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file',
				**FILEOPENOPTIONS)
	        if file != None:
			limpiar_areas()
			abrir_en_editor(file.name)	      
 
    def guardar_archivo_a_compilar(self):
		self.archivoacompilar = "/tmp/archivo"+self.PUERTOyPS+".s"
		tub = Popen(['rm', self.archivoacompilar], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		tub = Popen(['touch', self.archivoacompilar], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]
		tmp = open(self.archivoacompilar, "w")
	    	if tmp != None:
	        	# data = area5.get('1.0', END+'-1c')
	        	data = self.paneles.panel_leer(self.paneles.area5)
	        	tmp.write(data)
	        	tmp.close()

			archivotmppwd = "archivo"+self.PUERTOyPS+".s"
			tub = Popen(['cp', self.archivoacompilar, archivotmppwd], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
			streamdata = tub.communicate()[0]
	

    def save_command(self):
	    file = tkFileDialog.asksaveasfile(mode='w')
	    if file != None:
	    # slice off the last character from get, as an extra return is added
	        # data = area5.get('1.0', END+'-1c')
	        data = self.paneles.panel_leer(self.paneles.area5)
	        file.write(data)
	        file.close()
		self.archivoactual = file.name
                print self.archivoactual
         
    def exit_command(self):
	    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
	        root.destroy()
	 
    def about_command(self):
	    label = tkMessageBox.showinfo("Acerca de", "MIPSX - GUI for gdb multiarch\n\nEntorno de desarrollo en lenguaje assembler arquitectura MIPS\nEste programa ensabla, genera el programa ejecutable, y lo ejecuta en modo debug en una maquina MIPS real\n\nCopyright 2014 Rafael Ignacio Zurita\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")
		         
 
    def dummy(self):
	    print "I am a Dummy Command, I will be removed in the next step"

    def no_hacer_nada(self):
		print "nada por hacer"

    def archivo_sin_guardar(self):
		# data = area5.get('1.0', END+'-1c')
		data = self.paneles.panel_leer(self.paneles.area5)
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
		ip_mips = "10.0.15.50"
		tub = Popen(['mipsx_finalizar_gdbserver.sh', ip_mips, self.PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]

		tmp = "/tmp/archivo"+self.PUERTOyPS+".s"
		tmp2 = "archivo"+self.PUERTOyPS+".s"
		tmp3 = "/tmp/archivo"+self.PUERTOyPS+".s.elf"
		tmp4 = "/tmp/archivotemp"+self.PUERTOyPS+".txt"
		tub = Popen(['rm', tmp, tmp2, tmp3, tmp4], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		streamdata = tub.communicate()[0]



		quit()


        


 
 

def main():
  
	root.mainloop()  





if __name__ == '__main__':
	p = Popen(['gdb-multiarch'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	root = Tk()    

	# Para expandir cuando las ventanas cambian de tamao 
	root.columnconfigure(0,weight=1)
	root.rowconfigure(0, weight=1)

    	app = MipsxControl(root)
	main()  






