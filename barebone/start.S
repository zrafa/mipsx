/*
 * Copyright (C) 2001 MontaVista Software Inc.
 * Author: Jun Sun, jsun@mvista.com or jsun@junsun.net
 *
 * This program is free software; you can redistribute  it and/or modify it
 * under  the terms of  the GNU General  Public License as published by the
 * Free Software Foundation;  either version 2 of the  License, or (at your
 * option) any later version.
 *
 */

// #include "regdef.h"
// #include "cp0regdef.h"
#include "asm.h"
.data
	memoria: .asciiz "Hola mundo!"


.text
LEAF(_start)
	
	.set	mips2
	.set	reorder

	/* Disable interrupts */
	mtc0	zero, CP0_STATUS

        /* Disable watch exception. */
        mtc0    zero, CP0_WATCHLO
        mtc0    zero, CP0_WATCHHI

	/* disable kernel mode cache */
	mfc0	t0, CP0_CONFIG
	and	t0, ~0x7
	ori	t0, 0x2
	mtc0	t0, CP0_CONFIG

	/* set up stack */
	li	sp, 0xa0000000 + RAMSIZE - 16

	li t2, 0x9f000900
	li t3, 0x9f000928

	espera_tecla:
		lw t4, 0(t3)
		andi t4, t4, 0x01
		beq t4, zero, espera_tecla
	lw t1, 0(t2) 


	espera:
		lw t4, 0(t3)
		andi t4, t4, 0x20
		beq t4, zero, espera
	sw t1, 0(t2)
	
	/* jump to main */
	/* jal	main */
			
loop:
	j	loop
	nop
END(_start)

