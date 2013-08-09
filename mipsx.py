
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style


class Example(Frame):
  


    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
    	def prox_instruccion():
 		area2.insert("0.0"," que tal como te va")

        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        lbl = Label(self, text="Registros                                      GDB en MIPS - MR3020")
        lbl.grid(row=1,sticky=W, pady=4, padx=5)
        

        area1 = Text(self,height=13,width=80)
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
        
              
def salir():
	quit()


def main():
  
    root = Tk()
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
