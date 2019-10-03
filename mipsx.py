#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original del ejemplo de una aplicacion Tk: Jan Bodnar
last modified: December 2010 website: www.zetcode.com

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

class Mipsx(Frame):

     def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent
        self.ejecucion = False

        def prox_instruccion():
                p.stdin.write('step 1\n')

                mostrar_en(area4, "proximo")

                estado()
                if self.ejecucion:
                        memoria()
                        registros()
                        listado()

        def ejecutar():
                while self.ejecucion:
                        prox_instruccion()

        def salida(w, findelinea):
                w.delete("1.0", END)

                a = p.stdout.readline()
                while not findelinea in a:
                        # Esto es para saber si la ejecucion termino'.
                        # TODO: Hay que quitarlo de este metodo. Donde ponerlo?
                        if "No stack" in a:
                                self.ejecucion = False
                                w.insert(END,'\n\nEjecucion FINALIZADA\n\n')

                        a = a.replace('(gdb) ', '')

                        # Lo que sigue es una horrorosa manera de evitar los mensajes fieros de gdb
                        if not "help" in a:
                                if not "http" in a:
                                        if "Breakpoint" in a:
                                                w.delete("1.0", END)
                                                w.insert(END,'\n\nENSAMBLADO (compilacion) OK. Programa cargado.\n\n')
                                        w.insert(END,a)
                        a = p.stdout.readline()

        def mostrar_en(w, findelinea):
                p.stdin.write(findelinea)
                p.stdin.write('\r\n')
                salida(w, findelinea)

        def mostrar_en_depuracion():

                file = open("/tmp/archivotemp"+PUERTOyPS+".txt")
                contents = file.read()
                #area4.delete('1.0',END)
                area4.insert(END,contents)
                file.close()

        def memoria():
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
                p.stdin.write('x/40xw main\n')
                p.stdin.write('x/128 $sp - 128\n')
                mostrar_en(area3, "memoria")

        def estado():
                p.stdin.write('info frame\n')
                mostrar_en(area4, "estado")
                file = open("/tmp/archivotemp"+PUERTOyPS+".txt")
                contents = file.readline()
                while not "Remote" in contents:
                        print contents
                        area4.insert(END,contents)
                        contents = file.readline()

                area4.insert(END,"----------------------------------------\nSalida Estandar : \n\n")

                contents = file.read()
                file.close()
                area4.insert(END,contents)
                area4.see(END)

        def registros():
                p.stdin.write('info register\n')
                mostrar_en(area1, "registros")

        def listado():
                p.stdin.write('list 1,100\n')
                # p.stdin.write('disas main \n')
                p.stdin.write('disas \n')
                mostrar_en(area2, "listado")
                area2.see(END)

        def compilarparamalta():
                area4.delete('1.0',END)
                area4.insert('1.0',"Compilando para la malta ...\r\n")
                root.update_idletasks()

                p.stdin.write('detach \n')
                guardar_archivo_a_compilar()
                tub = Popen(['mipsx_compilarycargarparamalta.sh', self.archivoacompilar, PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]
                mostrar_en_depuracion()

                if tub.returncode == 0:
                        area4.insert(END, "Compilacion Finalizada \n")
                else:
                        area4.insert(END, "\n\nERROR al compilar y cargar\n\n")
                        mostrar_en_depuracion()

        def compilarycargar():
                area4.delete('1.0',END)
                area4.insert('1.0',"Compilando y Cargando ...\r\n")
                root.update_idletasks()

                p.stdin.write('detach \n')
                guardar_archivo_a_compilar()
                tub = Popen(['mipsx_compilarycargar.sh', self.archivoacompilar, PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]
                mostrar_en_depuracion()

                if tub.returncode == 0:
                        area4.insert(END, "Compilacion y carga : OK\n")

                        # ejecutable = self.archivoactual+".elf"
                        # ejecutable = ntpath.basename(ejecutable)
                        ejecutable = self.archivoacompilar+".elf"
                        ejecutable = ntpath.basename(ejecutable)

                        # Nos conectamos al gdbserver
                        # ip_mips="10.0.15.232"
                        # ip_mips="192.168.0.71"

                        ip_mips="10.0.15.50"
                        #comando='target extended-remote '+ip_mips+':'+PUERTOyPS+'\n'
                        comando='target remote '+ip_mips+':'+PUERTOyPS+'\n'
                        p.stdin.write(comando)

                        # gdbfile = 'set remote exec-file /tmp/'+ejecutable+'\n'
                        # p.stdin.write(gdbfile)
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
                        # p.stdin.write('run\n')
                        p.stdin.write('continue\n')
                        self.ejecucion = True

                        mostrar_en(area4,"estado")
                        area4.see(END)
                        memoria()
                        registros()
                        listado()
                else:
                        area4.insert(END, "\n\nERROR al compilar y cargar\n\n")
                        mostrar_en_depuracion()

        PUERTOyPS=str( random.randrange(4000,8000+1) )
        # PUERTOyPS="4567"

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

        area1 = Text(self,height=12,width=80)
        area1.grid(row=2, column=2, columnspan=1, rowspan=5,
            sticky=E+W+S+N)

        lbl = Label(self, text="Programa en Assembler y Programa Binario Decodificado (disassemble)")
        lbl.grid(row=7, column=2, pady=1, padx=1, sticky=W+N+E+S)

        area2 = Text(self, height=6,width=80)
        area2.grid(row=8, column=2, columnspan=1, rowspan=5,
            padx=1, sticky=E+W+S+N)

        lbl = Label(self, text='Memoria - Segmento de datos (debe existir la etiqueta "memoria") - Segmento de texto - Pila')
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

        # Variables globales
        archivoactual = "hello.s"
        archivoacompilar = "hello.s"
        archivotemp = "/tmp/archivotemp"+PUERTOyPS+".txt"
        # ip_mips = "10.0.15.232"
        ip_mips = "10.0.15.50"
        # ip_mips = "192.168.0.71"

        # Al abrir un archivo deseamos tener un area de trabajo cero
        def limpiar_areas():
                area4.delete('1.0',END)
                area3.delete('1.0',END)
                area2.delete('1.0',END)
                area1.delete('1.0',END)

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
                        limpiar_areas()
                        abrir_en_editor(file.name)

        def guardar_archivo_a_compilar():
                self.archivoacompilar = "/tmp/archivo"+PUERTOyPS+".s"
                tub = Popen(['rm', self.archivoacompilar], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]
                tub = Popen(['touch', self.archivoacompilar], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]
                tmp = open(self.archivoacompilar, "w+b")
                if tmp != None:
                        data = area5.get('1.0', END+'-1c')
                        data3 = u''.join(data).encode('utf-8').strip()
                        print(data3)
                        tmp.write(data3)
                        tmp.close()

                        archivotmppwd = "archivo"+PUERTOyPS+".s"
                        tub = Popen(['cp', self.archivoacompilar, archivotmppwd], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                        streamdata = tub.communicate()[0]

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
            label = tkMessageBox.showinfo("Acerca de", "MIPSX - GUI for gdb multiarch\n\nEntorno de desarrollo en lenguaje assembler arquitectura MIPS\nEste programa ensabla, genera el programa ejecutable, y lo ejecuta en modo debug en una maquina MIPS real\n\nCopyright 2014 Rafael Ignacio Zurita\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")

        def dummy():
            print "I am a Dummy Command, I will be removed in the next step"

        def no_hacer_nada():
                print "nada por hacer"

        def archivo_sin_guardar():
                data = area5.get('1.0', END+'-1c')
                fd = open(self.archivoactual)
                contents = fd.read()
                fd.close()
                if data == contents:
                        return False
                res = tkMessageBox.askquestion("Confirmar", "Archivo sin guardar\nEsta seguro de finalizar el programa?", icon='warning')
                if res == 'yes':
                        return False
                return True

        def salir():
                if archivo_sin_guardar():
                        return

                tmp = "/tmp/archivo"+PUERTOyPS+".s"
                tmp2 = "archivo"+PUERTOyPS+".s"
                tmp3 = "/tmp/archivo"+PUERTOyPS+".s.elf"
                tmp4 = "/tmp/archivotemp"+PUERTOyPS+".txt"
                tub = Popen(['rm', tmp, tmp2, tmp3, tmp4], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]

                tmp2 = "/tmp/archivo"+PUERTOyPS+".s.o"
                ip_mips = "10.0.15.50"
                tub = Popen(['mipsx_finalizar_gdbserver.sh', ip_mips, PUERTOyPS, tmp, tmp2, tmp3, tmp4], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                streamdata = tub.communicate()[0]
                # ip_mips = "10.0.15.232"
                # ip_mips = "192.168.0.71"
                # killgdbserver = Popen(['sshpass', '-p', clave, 'ssh', '-o', 'StrictHostKeyChecking=no', '-l', 'root', ip_mips, comando], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
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

        menu.add_command(label="Run", command=ejecutar)
        menu.add_command(label="Next", command=prox_instruccion)
        menu.add_command(label="Breakpoint", command=no_hacer_nada)
        menu.add_command(label="Compilar y Cargar", command=compilarycargar)
        menu.add_command(label="Compilar y Ejecutar en Malta", command=compilarparamalta)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Ayuda", menu=helpmenu)
        helpmenu.add_command(label="Acerca de...", command=about_command)
        menu.add_command(label="Salir", command=salir)
        abrir_en_editor("hello.s")

        # para que al cerrar la ventana cierre los temporales y los borre
        root.protocol("WM_DELETE_WINDOW", salir)

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
