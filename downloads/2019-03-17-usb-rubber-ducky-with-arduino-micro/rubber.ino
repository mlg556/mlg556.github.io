#include "Keyboard.h"

const char cmd[] PROGMEM = {};
char chr;


void typer() {
    for (int i = 0; i < strlen_P(cmd); i++) {
        chr = pgm_read_byte_near(cmd + i);
        Keyboard.write(chr);
    }
}

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


void setup() {
    Keyboard.begin();
    delay(500);
    cmdOpen();
    typer();
    Keyboard.write(KEY_RETURN);
}

void loop() {}
