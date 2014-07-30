



#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

import time
import sys
from subprocess import Popen, PIPE, STDOUT

#from Tkinter import Tk, Text, BOTH, W, N, E, S
from Tkinter import *
from ttk import Frame, Button, Label, Style

# Para el menu FILE
from tkFileDialog import askopenfilename

# Para extrar el nombre de archivo sin ruta
import ntpath


class Example(Frame):
  


    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
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



        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        lbl = Label(self, text="Registros                                      GDB en MIPS - MR3020")
        lbl.grid(row=1,sticky=W, pady=4, padx=5)
        

        area1 = Text(self,height=15,width=80)
        area1.grid(row=2, column=0, columnspan=1, rowspan=5, 
            sticky=E+W+S+N)
        
        lbl = Label(self, text="Programa en Assembler")
        lbl.grid(row=7,pady=1, padx=1, sticky=W+N+E+S)
        
    	area2 = Text(self, height=12,width=80)
        area2.grid(row=8, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text="Memoria")
        lbl.grid(row=13,pady=1, padx=1, sticky=W+N+E+S)

        area3 = Text(self,height=15,width=80)
        area3.grid(row=14, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)

        lbl4 = Label(self, text="Mensajes de Depuracion")
        lbl4.grid(row=19,pady=1, padx=1, sticky=W+N+E+S)

        area4 = Text(self,height=8,width=80)
        area4.grid(row=20, column=0, columnspan=1, rowspan=5, 
            padx=1, sticky=E+W+S+N)


        abtn = Button(self, text="SALIR",command=salir)
        abtn.grid(row=2, column=1, padx=10, sticky=W)

        cbtn = Button(self, text="Run")
        cbtn.grid(row=3, column=1, padx=10, sticky=W)
        
        cbtn3 = Button(self, text="Next", command=prox_instruccion)
        cbtn3.grid(row=4, column=1, padx=10, sticky=W)
        
        cbtn4 = Button(self, text="Breakpoint")
        cbtn4.grid(row=5, column=1, padx=10, sticky=W)
        
#	#p = Popen(['/home/rafa/openwrt/attitude_adjustment/staging_dir/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-gdb', 'add'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

#	p = Popen(['/home/rafa/programacion/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-uclibc-gdb', 'add'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

#	p.stdin.write('target remote 192.168.0.71:4567\n')
#	p.stdin.write('\r\n')
#	salida(area4)


def salir():
	clave = "root"
	comando = "killall gdbserver"
	killgdbserver = Popen(['sshpass', '-p', clave, 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@192.168.0.71', comando], stdout=PIPE, stdin=PIPE, stderr=STDOUT)	
	quit()


def main():
  
   	
    	app = Example(root)
    
	# Para el menu FILE
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Abrir", command=openfile)
	filemenu.add_separator()
	filemenu.add_command(label="Salir", command=root.quit)
	menubar.add_cascade(label="Archivo", menu=filemenu)
	root.config(menu=menubar)

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


#	salida(area4)

if __name__ == '__main__':
	p = Popen(['/home/rafa/programacion/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-uclibc-gdb'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	root = Tk()    
	main()  






