
import time
import sys
from subprocess import Popen, PIPE, STDOUT

def salida():
        a = p.stdout.readline()
        while not "(gdb)" in a:
                sys.stdout.write(a)
                # print a
                a = p.stdout.readline()


def registros():
        p.stdin.write('info register\n')
        salida()

def listado():
        p.stdin.write('list 0\n')
        salida()


p = Popen(['/home/rolo/opt/crossdev/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-lin=PIPE, stdin=PIPE, stderr=STDOUT)

p.stdin.write('target remote 10.0.15.166:4567\n')
salida()

time.sleep(2)
p.stdin.write('list\n')
salida()

time.sleep(2)

registros()
time.sleep(2)
listado()
time.sleep(2)

p.stdin.write('run\n')
salida()

time.sleep(2)

