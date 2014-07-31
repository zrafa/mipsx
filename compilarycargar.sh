#!/bin/bash

( /home/rafa/programacion/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-uclibc-as -g --gstabs $1 -o ${1}.o 2>&1 ) > /tmp/archivotemp.txt  &&

( /home/rafa/programacion/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-uclibc-ld -static -o ${1}.elf ${1}.o 2>&1 ) > /tmp/archivotemp.txt  &&

( sshpass -p "root" scp ${1}.elf root@192.168.0.71:/tmp 2>&1 ) >> /tmp/archivotemp.txt &&

(EJECUTABLE=`basename ${1}.elf`;  echo $EJECUTABLE; sshpass -p "root" ssh -o StrictHostKeyChecking=no root@192.168.0.71 "gdbserver 0.0.0.0:4567 /tmp/$EJECUTABLE" 2>&1 & ) >> /tmp/archivotemp.txt

