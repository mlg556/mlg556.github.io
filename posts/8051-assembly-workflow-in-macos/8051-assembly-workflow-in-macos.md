---
title: "8051 Assembly Workflow in macOS"
date: 14 February 2019
---

Intel 8051 is a microcontroller unit developed in 1980s. On the off chance that you are writing [Assembly](https://en.wikipedia.org/wiki/Assembly_language) code for this arcane technology, this post will exemplify a workflow on how to code, simulate and embed your program in a [AT89S52/51](https://www.microchip.com/wwwproducts/en/at89s52) microchip.

# Requirements

## Arduino

We will be using an [Arduino](https://www.arduino.cc) board to act as an [ISP programmer](https://www.arduino.cc/en/tutorial/arduinoISP). Pretty much any model will do, I will be using an [Arduino Nano](https://store.arduino.cc/usa/arduino-nano). Obviously, you will also need the [IDE](https://www.arduino.cc/en/Main/Software) to program the Arduino board first. You *could* in theory do this with an [USBasp](https://www.fischl.de/usbasp/), but for the device to support AT89S52 series, you have to update the firmware: which again requires an Arduino, so why not just cut the middle man.

## AVRDUDE

[AVRDUDE](https://www.nongnu.org/avrdude/) is a command line utility which will be used to write the generated `.hex` file in to the ROM of the microchip. You can install it with `brew install avrdude`. Since the default config file does not support AT89S52, we will use a modified version provided by [varun96](https://www.instructables.com/id/Programming-AT89s52-Using-USBasp-ISP-Programmer/). It can be downloaded via the Instructables site, or directly here: [F40R96CIUSLFZFP.conf](files/F40R96CIUSLFZFP.conf). Put this file somewhere accessible, we will later refer to it.

## C51ASM

_C51ASM_ is an assembler written by Atmel (which is now called _Microchip_) for the 8051 architecture, supporting the AT89S52 we are using. However, perhaps because of the acquirement by _Microchip_, the link for the product [http://www.atmel.com/tools/C51ASM.aspx](http://www.atmel.com/tools/C51ASM.aspx) no longer works. Fortunately, by the magic of *WayBackMachine*, I was able to connect to an archived version and download the executable. [Here](https://web.archive.org/web/20160410011650/http://www.atmel.com/tools/C51ASM.aspx) is the link for the archived webpage, and [c51asm_macosx_1-2.zip](files/c51asm_macosx_1-2.zip) is the macOS version which can be directly downloaded. Make sure to extract the files in the correct places, perhaps `/usr/local/bin` and `usr/local/include`.

## 8051 emulator
Jari Komppa's [8051 emulator](http://sol.gfxile.net/8051.html) is a simple emulator which you can run in the Terminal since the UI is based on _ncurses_. The [pre-built OSX Intel binary version](http://sol.gfxile.net/zip/emu8051_072.dmg) worked fine for me. It achieves faster than real-time simulations which are great for simulating code such as a blinking LED etc...

# Simulation
Let us try to simulate this basic code, which sums decimal `3` and `4` and stores the result in the `A`(or `ACC`) register of the chip.

```nasm
ORG 0H
    MOV A, #3
    MOV R2, #4
    ADD A, R2
END

```
First we have to assemble the code. Assuming that the file name is `sum.asm`:

```bash
~$ c51asm sum.asm
C51ASM: advanced C51 macro assembler Version 1.2 (06 May 2011)
Copyright (C) 2011 Atmel Corp.


Pass 1 completed with no warnings and no errors

Pass 2 completed with no warnings and no errors

Segment usage:
   Code      :      5 bytes
   Data      :      0 bytes
   Idata     :      0 bytes
   Edata     :      0 bytes
   Fdata     :      0 bytes
   Xdata     :      0 bytes
   Bit       :      0 bits

   Register banks used: ---

   Warnings: 0
   Errors:   0
```

The assembler ran without any errors, and generated the file `sum.hex` which we will use to simulate the code. When you run the `8051 emulator` you have downloaded, you will be presented with a screen like this:

![Emulator start.](images/emu0.png)

You can load the generated `.hex` file by pressing `L` and entering the file name (`sum.hex` in our case).

![Emulator load file.](images/emu1.png)

Now the emulator will show the assembly code on the bottom left, and the real-time values of various registers and memory elements. Since we do not want to simulate this code in real-time, we can simply press `SPACE` to _step_ the simulation. We can see the assembly code executed and the results:

![Emulator assembly code.](images/emu2.png)

![Emulator registers.](images/emu3.png)

To run a simulation in real-time (or faster), you have to press `R` and adjust the simulation speed with `+-` keys.

This code won't be of much use when embedded in the microchip. Let us simulate another code, designed to blink a LED.

```nasm
; LED blinker.
; total period = ((256 * 24 * PER) / 12000) milliseconds
; = 0.5 * PER milliseconds
; on-time = 0.25 * PER

        ORG 0H
        EQU PER EQU 2

MAIN:   ACALL   ON
        ACALL   DELAY
        ACALL   OFF
        ACALL   DELAY
        AJMP    MAIN

ON:     SETB    P1.0
        RET

OFF:    CLR     P1.0
        RET

DELAY:  MOV     R0, #PER ; generate delay, for 0.5 * PER ms
        MOV     R1, #0

LOOP:   DJNZ    R1, LOOP
        DJNZ    R0, LOOP
        RET

        END
```

As before, run `as31 blink.asm`, and load the `.hex` file to the emulator. Satisfied with the simulation, we can finally embed the program to the AT89S52.

# Programming

First, we will have to configure the Arduino board to act as the ISP programmer. To do this, open the Arduino IDE. Then open *File>Examples>ArduinoISP*. This is the sketch we will be uploading to the Arduino, but first, uncomment the line `#define USE_OLD_STYLE_WIRING
`(You can alternatively use the ICSP headers, but I have found this to be less problematic.) Go on and click _Upload_ and program the Arduino.

## Connections

Now that we have configured the Arduino board, we have to make the necessary connections. Before interconnecting the two chips, first put a 10 $\mu F$ capacitor between the `RST` pin and `GND` of the Arduino board. This prevents the auto-reset function interfering with the programming we are about to do. After that, the AT8952 chip requires a crystal oscillator and some capacitors to function. This schematic from [ernstc.dk](http://ernstc.dk/arduino/at89s.html) shows the basic idea:

![Programming At89s5x.](images/conn.jpg)

After this, you have to wire the Arduino to the AT89S52. The ArduinoISP sketch that we have uploaded has configured the pins 10 as `RESET`, 11 as `MISO`, 12 as `MOSI` and 13 as `SCK`. This means that the connections are:

| Arduino Pin | AT89S52 Pin |
|-------------|-------------|
| D10 (RESET) | 9 (RST)     |
| D11 (MISO)  | 6 (MOSI) (P1.5)   |
| D12 (MOSI)  | 7 (MISO) (P1.6)   |
| D13 (SCK)   | 8 (SCK)  (P1.7)   |
| 5V         | 40 (VCC), 31 (EA/VPP)   |
| GND         | 20 (GND)   |

## Flashing

After triple-checking the connections, it is time to flash the program to the microchip memory. The command will have the form:

```bash
avrdude \
-C PATH_TO_CONFIG_FILE -c stk500v1 \
-P ARDUINO_PORT -p 89s52 -b 19200 \
-U flash:w:PATH_TO_HEX_FILE \
```

`PATH_TO_CONFIG_FILE` is the path of the modified config file `F40R96CIUSLFZFP.conf` that we have downloaded. To find which port your Arduino is connected to, check it in the Arduino IDE or on a terminal enter `ls /dev/cu.*` to list all connected serial devices.

Make sure to check the output of this command; most importantly, it has to return the correct device signature. If it returns `0x0000`, or `Yikes!  Invalid device signature.`, check your connections again. _DO NOT_ "_use -F to override this check._" After flashing the code, you can also verify it by changing the letter `w`(write) to `v`(verify) in the `avrdude` command.

# Summary

Assuming `c51asm` points to the _c51asm assembler_, `emu` points to the _8051 emulator_, `PATH_TO_CONFIG_FILE` is the location of the modified `F40R96CIUSLFZFP.conf` file and `PATH_TO_ARDUINO` is the name of the serial port which the Arduino board is connected (something like `/dev/cu.usbserial-A9OZNH9X` in macOS), the following utility summarizes the workflow.

```bash
#!/bin/bash

if [ "$1" == 'ass' ]; then
    c51asm $2.asm -l --target AT89S52
elif [ "$1" == 'sim' ]; then
    emu $2.hex
elif [ "$1" == 'prg' ]; then
    avrdude -C PATH_TO_CONFIG_FILE -c stk500v1 -P `ARDUINO_PORT` -p 89s52 -b 19200 -U flash:w:$2.hex
else
    echo "asm v1.1 -- @mlg556
Usage:
  asm (ass | sim | prg)
Options:
  ass    		Assemble using as32
  sim	 		Simulate the assembled .hex
  prg    		Write .hex to flash"
fi

```
