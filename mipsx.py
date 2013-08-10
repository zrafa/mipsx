
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


class Example(Frame):
  


    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
    	def prox_instruccion():
 		# area2.insert("0.0"," que tal como te va")
		registros()

	def salida(w):
		w.delete("1.0", END)
		w.insert(END,"\n")
		a = p.stdout.readline()
		while not "(gdb)" in a:
			#sys.stdout.write(a)
 			w.insert(END,a)
			# print a
			a = p.stdout.readline()
	

	def registros():
		p.stdin.write('info register\n')
		salida(area1)
		p.stdin.write('\r\n')
		salida(area1)

	def listado():
		p.stdin.write('list 0\n')
		salida()


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
        
	p = Popen(['/home/rafa/openwrt/attitude_adjustment/staging_dir/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-gdb', 'add'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	p.stdin.write('target remote 192.168.1.1:4567\n')
	p.stdin.write('\n')
	salida(area3)
	

              
def salir():
	quit()


def main():
  
    root = Tk()
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  







#registros()
#time.sleep(2)
#listado()
#time.sleep(2)
#
#p.stdin.write('run\n')
#salida()
#
#time.sleep(2)
