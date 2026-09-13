#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Versión convertida a Python 3 del script mipsx.py
Basado en el original de Rafael Ignacio Zurita
Facultad de Informática - Universidad Nacional del Comahue
"""

import time
import sys
import random
import os
import ntpath
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText
from subprocess import Popen, PIPE, STDOUT

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")):
            self.event_generate("<<Change>>", when="tail")
        return result


class TextLineNumbers(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.text_widget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=("Courier New", 10))
            i = self.text_widget.index(f"{i}+1line")

class Mipsx(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ejecucion = False
        self.archivoactual = "hello.s"
        self.archivoacompilar = "hello.s"
        self.PUERTOyPS = str(random.randrange(4000, 8001))
        self.archivotemp = f"/tmp/archivotemp{self.PUERTOyPS}.txt"
        self.ip_mips = "10.0.2.50"

        self.parent.title("Mipsx - GUI for gdb multiarch")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)

        for i in range(3):
            self.columnconfigure(i, weight=1)
        for i in range(20):
            self.rowconfigure(i, weight=1)

        tk.Label(self, text="Registros                                      GDB en MIPS - MR3020").grid(row=1,column=2, sticky=tk.W, pady=4, padx=5)
        
        self.area1 = tk.Text(self, height=12, width=80)
        self.area1.grid(row=2, column=2, rowspan=5, sticky="nsew")

        tk.Label(self, text="Programa en Assembler y Programa Binario Decodificado (disassemble)").grid(row=7, column=2, pady=1, padx=1, sticky="nsew")
        
        self.area2 = tk.Text(self, height=6, width=80)
        self.area2.grid(row=8, column=2, rowspan=5, padx=1, sticky="nsew")

        tk.Label(self, text='Memoria - Segmento de datos (debe existir la etiqueta "memoria") - Segmento de texto - Pila').grid(row=13, column=2, pady=1, padx=1, sticky="nsew")
        self.area3 = tk.Text(self, height=15, width=80)
        self.area3.grid(row=14, column=2, rowspan=5, padx=1, sticky="nsew")

        tk.Label(self, text="Mensajes de Depuracion").grid(row=13, column=0, pady=1, padx=1, sticky="nsew")
        self.area4 = tk.Text(self, height=8, width=60)
        self.area4.grid(row=14, column=0, rowspan=5, padx=1, sticky="nsew")

        tk.Label(self, text="Editor del Programa").grid(row=1,column=0, sticky=tk.W, pady=4, padx=5)


        # Creamos el area5
        #self.area5 = ScrolledText(self, height=20, width=60)
        #self.area5.grid(row=2, column=0, rowspan=10, padx=1, sticky="nsew")

        editor_frame = tk.Frame(self)
        editor_frame.grid(row=2, column=0, rowspan=10, padx=1, sticky="nsew")

        vsb = tk.Scrollbar(editor_frame, orient="vertical")
        self.area5 = CustomText(editor_frame, height=20, width=60, wrap="none",
                         yscrollcommand=vsb.set, font=("Courier New", 10))
        vsb.config(command=self.area5.yview)

        self.linenumbers = TextLineNumbers(editor_frame, self.area5, width=35,
                                    background="#eeeeee", highlightthickness=0)
        self.area5.bind("<<Change>>", self.linenumbers.redraw)
        self.area5.bind("<Configure>", self.linenumbers.redraw)

        self.linenumbers.pack(side="left", fill="y")
        self.area5.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.linenumbers.redraw()

        # FIN de Creamos el area5



        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="Archivo", menu=filemenu)
        filemenu.add_command(label="Nuevo", command=self.dummy)
        filemenu.add_command(label="Abrir...", command=self.open_command)
        filemenu.add_command(label="Guardar...", command=self.save_command)
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.salir)

        toolbar = tk.Frame(self)
        toolbar.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(2, 4))

        ttk.Button(toolbar, text="Run", command=self.ejecutar).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Next", command=self.prox_instruccion).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Breakpoint", command=self.no_hacer_nada).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Compilar y Cargar", command=self.compilarycargar).pack(side=tk.LEFT, padx=2)
        # ttk.Button(toolbar, text="Compilar y Ejecutar TPO 2019", command=self.compilarTPO2019).pack(side=tk.LEFT, padx=2)

        # menu.add_command(label="Run", command=self.ejecutar)
        # menu.add_command(label="Next", command=self.prox_instruccion)
        # menu.add_command(label="Breakpoint", command=self.no_hacer_nada)
        # menu.add_command(label="Compilar y Cargar", command=self.compilarycargar)
        # menu.add_command(label="  Compilar y Ejecutar TPO 2019  ", command=self.compilarTPO2019)

        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Ayuda", menu=helpmenu)
        helpmenu.add_command(label="Acerca de...", command=self.about_command)
        menu.add_command(label="Salir", command=self.salir)

        self.abrir_en_editor("hello.s")
        self.parent.protocol("WM_DELETE_WINDOW", self.salir)

    def dummy(self):
        print("I am a Dummy Command, I will be removed in the next step")

    def no_hacer_nada(self):
        print("nada por hacer")

    def salir(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def abrir_en_editor(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as fd:
                contents = fd.read()
                self.area5.delete('1.0', tk.END)
                self.area5.insert('1.0', contents)
                self.archivoactual = archivo
                print(self.archivoactual)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def open_command(self):
        file = filedialog.askopenfile(mode='r', defaultextension='*.s',
            filetypes=[('Archivo assembler','*.s'), ('Todos los archivos','*.*')])
        if file:
            self.abrir_en_editor(file.name)

    def save_command(self):
        file = filedialog.asksaveasfile(mode='w')
        if file:
            data = self.area5.get('1.0', tk.END+'-1c')
            file.write(data)
            file.close()
            self.archivoactual = file.name
            print(self.archivoactual)

    def estado(self):                                                                                                                                  
                p.stdin.write('info frame\n')                                                                                                          
                p.stdin.flush()
                self.mostrar_en(self.area4, "estado")                                                                                                            
                file = open("/tmp/archivotemp"+self.PUERTOyPS+".txt")                                                                                       
                contents = file.readline()                                                                                                             
                while not "Remote" in contents:                                                                                                        
                        # print contents
                        self.area4.insert(tk.END,contents)
                        contents = file.readline()
                                                                                                                                                       
                self.area4.insert(tk.END,"----------------------------------------\nSalida Estandar : \n\n")
                                                                                                                                                       
                contents = file.read()
                file.close()
                self.area4.insert(tk.END,contents)
                self.area4.see(tk.END)

    def prox_instruccion(self):
                p.stdin.write('step 1\n')
                p.stdin.flush()
                                                                                                                                                       
                self.mostrar_en(self.area4, "proximo")
                                                                                                                                                       
                self.estado()
                if self.ejecucion:
                        self.memoria()
                        self.registros()
                        self.listado()
                                                                                                                                                       
    def ejecutar(self):
                while self.ejecucion:
                        self.prox_instruccion()     

    def salida(self, w, findelinea):
        w.delete("1.0", tk.END)
                                
        a = p.stdout.readline()
        while findelinea not in a:
                        # Esto es para saber si la ejecucion termino'. 
                        # TODO: Hay que quitarlo de este metodo. Donde ponerlo?
               if "No stack" in a:
                    self.ejecucion = False
                    w.insert(tk.END,'\n\nEjecucion FINALIZADA\n\n')

               a = a.replace('(gdb) ', '')                             

               # Lo que sigue es una horrorosa manera de evitar los mensajes fieros de gdb
               if not "help" in a:
                    if not "http" in a:
                       if "Breakpoint" in a:
                           w.delete("1.0", tk.END)
                           w.insert(tk.END,'\n\nENSAMBLADO (compilacion) OK. Programa cargado.\n\n')
                       w.insert(tk.END,a)         
               a = p.stdout.readline()                 
        

    def mostrar_en(self, w, findelinea):
        p.stdin.write(findelinea)
        p.stdin.write('\r\n')
        p.stdin.flush()
        self.salida(w, findelinea)
        self.parent.update_idletasks()

    def mostrar_en_depuracion(self):
                
        file = open("/tmp/archivotemp"+self.PUERTOyPS+".txt")
        contents = file.read()
        #area4.delete('1.0',END)
        self.area4.insert(tk.END,contents)
        file.close()
        # root.update_idletasks()
        self.parent.update_idletasks()

    def memoria(self):
        # Para mostrar el segmento de datos, la etiqueta memoria debe estar al principio
        p.stdin.write('info address memoria\n')
        p.stdin.write('infomemoria\n')
        p.stdin.flush()
        print("2.0", flush=True)
        ## a = p.stdout.readline()
        a = "a"
        solicitar_seg_de_datos = ""
        print("2.1")
        while "infomemoria" not in a:
            print("a : " + a)
            if "Symbol " in a:
                a = a.replace('(gdb) Symbol "memoria" is at ', '')
                a = a.replace(' in a file compiled without debugging.', '')
                solicitar_seg_de_datos = "x/40xw " + a + "\n"
            a = p.stdout.readline()

        print("2.2")
        if solicitar_seg_de_datos == "":
            p.stdin.write('x/40xw $pc\n')
            p.stdin.flush()
        else:
            p.stdin.write(solicitar_seg_de_datos)
            p.stdin.flush()
        p.stdin.write('x/40xw main\n')
        p.stdin.write('x/128 $sp - 128\n')
        p.stdin.flush()
        self.mostrar_en(self.area3, "memoria")

    def registros(self):
        p.stdin.write('info register\n')
        p.stdin.flush()
        self.mostrar_en(self.area1, "registros")

    def listado(self):
          p.stdin.write('list 1,100\n')
          p.stdin.write('disas \n')
          p.stdin.flush()
          self.mostrar_en(self.area2, "listado")
          self.area2.see(tk.END)

    def leer_gdb(self):
        while True:
          linea = p.stdout.readline()
          if not linea:
            break
          print(linea, end="")      # sale en la consola de Python
          if "(gdb)" in linea:
            break

    def compilarycargar(self):
        self.area4.delete('1.0', tk.END)
        self.area4.insert('1.0', "Compilando y Cargando ...\n")
        self.parent.update_idletasks()

        archivo_tmp = f"/tmp/archivo{self.PUERTOyPS}.s"
        with open(archivo_tmp, "w", encoding="utf-8") as f:
            #codigo = self.area5.get('1.0', tk.END).strip()
            codigo = self.area5.get('1.0', tk.END).strip() + "\n"
            f.write(codigo)
            # f.write("\n") 

        # comando = ["mipsx_compilarycargar.sh", archivo_tmp, self.PUERTOyPS]
        tub = Popen(['mipsx_p3_compilarycargar.sh', archivo_tmp, self.PUERTOyPS, self.ip_mips], stdout=PIPE, stdin=PIPE, stderr=STDOUT, pipesize=1024*1024,)
        streamdata = tub.communicate()[0]
        self.mostrar_en_depuracion()

        if tub.returncode == 0:
            self.area4.insert(tk.END, "Compilacion y carga : OK\n")


            # ejecutable = self.archivoacompilar+".elf"
            ejecutable = archivo_tmp+".elf"
            ejecutable = ntpath.basename(ejecutable)

            p.stdin.write('disconnect \n')
            p.stdin.write('remove-inferiors 1\n')
            p.stdin.flush()
            # Nos conectamos al gdbserver
            comando='target remote '+self.ip_mips+':'+self.PUERTOyPS+'\n'
            p.stdin.write(comando)
            p.stdin.flush()

            # gdbfile = 'set remote exec-file /tmp/'+ejecutable+'\n'
            # p.stdin.write(gdbfile)
            # Respondemos "y"es a recargar                  
            p.stdin.write('y \n')
            p.stdin.flush()

            # Abrimos con gdb el archivo ejecutable
            gdbfile = 'file /tmp/'+ejecutable+'\n'
            p.stdin.write(gdbfile)
            # Respondemos "y"es a recargar                  
            p.stdin.write('y \n')
            print("1")
                
            p.stdin.write('delete \n')
            p.stdin.write('y \n')
            p.stdin.write('break main\n')
            # p.stdin.write('run\n')
            # p.stdin.write('continue\n')
            print("2")
            self.ejecucion = True

            self.mostrar_en(self.area4,"estado")
            self.area4.see(tk.END)
            self.memoria()
            print("3")
            self.registros()
            print("4")
            self.listado()
            print("5")
        else:
            self.area4.insert(tk.END, "\n\nERROR al compilar y cargar\n\n")
            self.mostrar_en_depuracion()

        # comando = ["mipsx_compilarycargar.sh", archivo_tmp, self.PUERTOyPS, self.ip_mips]
        # proceso = Popen(comando, stdout=PIPE, stderr=STDOUT, text=True)
        # salida, _ = proceso.communicate()

        # self.area4.insert(tk.END, salida)
        # self.area4.insert(tk.END, f"\nProceso finalizado con código: {proceso.returncode}\n")
        # self.area4.see(tk.END)
        # self.ejecucion = (proceso.returncode == 0)

    def compilarTPO2019(self):
        self.area4.delete('1.0', tk.END)
        self.area4.insert('1.0', "\nCompilando TPO2019 ...\n")
        self.parent.update_idletasks()

        archivo_tmp = f"/tmp/archivo{self.PUERTOyPS}.s"
        with open(archivo_tmp, "w", encoding="utf-8") as f:
            codigo = self.area5.get('1.0', tk.END).strip()
            f.write(codigo)

        comando = ["mipsx_p3_compilarycargarTPO2019.sh", archivo_tmp, self.PUERTOyPS]
        proceso = Popen(comando, stdout=PIPE, stderr=STDOUT, text=True)
        salida, _ = proceso.communicate()

        self.area4.insert(tk.END, salida)
        self.area4.insert(tk.END, f"\nProceso finalizado con código: {proceso.returncode}\n")
        self.area4.see(tk.END)
        self.ejecucion = (proceso.returncode == 0)

    def about_command(self):
        messagebox.showinfo("Acerca de", "MIPSX - GUI for gdb multiarch\n\nEntorno de desarrollo en lenguaje assembler arquitectura MIPS\nEste programa ensambla, genera el programa ejecutable y lo ejecuta en modo debug en una máquina MIPS real\n\nFacultad de Informática\nUniversidad Nacional del Comahue")


def main():
    global p
    # p = Popen(['gdb-multiarch'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p = Popen(['gdb-multiarch'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True)
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = Mipsx(root)
    root.mainloop()


if __name__ == '__main__':
    main()
