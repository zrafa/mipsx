CC=mipsel-linux-gcc

CFLAGS=-Wall -g

.PHONY:		all clean spotless

all:
	/home/lechnerm/rafa/mr3020/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-as -g --gstabs -o serial.o serial.s
	/home/lechnerm/rafa/mr3020/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-gcc -g -c -o uartmips_init.o uartmips_init.c 
	/home/lechnerm/rafa/mr3020/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-gcc -o serial uartmips_init.o serial.o


clean:
		rm -f uartmips_init.o serial.o serial

