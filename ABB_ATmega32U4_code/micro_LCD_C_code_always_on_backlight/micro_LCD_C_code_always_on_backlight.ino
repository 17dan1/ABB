/*
   ABB M4M 2X Power Meter LCD 20x4
   Created: 20/03/2026
   Author: Emanuele Pace
   Note: Pure C coding is better :)

   ABB Power meter is configured to output 1 10ms pulse every Wh consumption, 2 channel is used,
   one for active and the other for reactive energy. This script uses TIMER 1 and EXTERNAL INTERRUPT
   to count the time between every pulse end, measure the time interval to extract and print to LCD the 
   power onsumption in kW and kVA.

   UPLOAD: To upload pure C Arduino code to the Arduino Micro (ATmega32U8), press the upload button, 
   then, during the upload phase, reset the microcontroller with the reset button.

   -- PIN MAPPING --
   PIN    PORT      USAGE
   2      PD1       INT1 input reactive energy pulse
   3      PD0       INT0 input active energy pulse
   13     PC7       LED_BUILDIN
   A0     PF7       LCD data bit 7
   A1     PF6       LCD data bit 6
   A2     PF5       LCD data bit 5
   A3     PF4       LCD data bit 4
   A4     PF1       LCD enable
   A5     PF0       LCD RS
*/

#define F_CPU 16000000UL
#include <util/delay.h>
#include <string.h>

volatile uint16_t differences[] = {0, 0};
volatile uint16_t capture_value_INT0 = 0;
volatile uint16_t capture_value_INT1 = 0;
volatile uint8_t no_signal_time_count[] = {0, 0};
volatile bool captured_flag_INT0 = false;
volatile bool captured_flag_INT1 = false;
volatile bool overflow_flag_INT0 = false;
volatile bool overflow_flag_INT1 = false;

uint8_t DDRAM [4][20] = {
  {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13},
  {0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53},
  {0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27},
  {0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67}
};

// Send data to LCD
void send_data(bool rs, uint8_t data ) {
  if (rs) PORTF |= (1 << PF0); else PORTF &= ~(1 << PF0);   // Set RS
  _delay_us(10);
  PORTF = (data & 0b11110000) | (PORTF & 0b00001111);   //Set Upper Nibble
  _delay_us(5);
  PORTF |= (1 << PF1);    // Send enable pulse
  _delay_us(10);
  PORTF &= ~(1 << PF1);
  PORTF = (data << 4) | (PORTF & 0b00001111);   //Set Lower Nibble
   _delay_us(5);
  PORTF |= (1 << PF1);    // Send enable pulse
  _delay_us(10);
  PORTF &= ~(1 << PF1);
  _delay_ms(5);
}

// Print ASCII Text to LCD
void print_string(char *str) {
  for(uint8_t i=0; i<strlen(str); i++) {
    send_data(1, str[i]);
  }
}

// Set LCD cursor position
void set_cursor(uint8_t row,  uint8_t column) {
  if (row > 3) row = 0;
  if (column > 19) column = 0;
  send_data(0, (DDRAM[row][column] | 0b10000000));
}

// // --- MAIN --- // //
int main() {
  const char *labels[] = { "Attiva", "Reattiva" };
  const char *units[] = { "kW    ", "kVAr    " };
  float times[] = { 0.0, 0.0 };
  float powers[] = { 0.0, 0.0 };
  char buffer[21];
  char float_buffer[10];
  // -- PORT SETUP --
  DDRF = 0xF3;    // Set bit 7,6,5,4,1,0 as output
  DDRD = (1 << PD7);  // Set bit 7 as output
  DDRC = 0b10000000;  // Set LED_BUILDIN as output
  // -- EXTERNAL INTERRUPT SETUP --
  cli();
  EICRA = 0; EIMSK = 0; // Clear external interrupts control registers
  EICRA |= 0b00001010;  // Falling edge on INT1 and INT0
  EIMSK |= (1 << INT0) | (1 << INT1); // Enable external interrupt INT1 and INT0
  EIFR &= ~((1 << INTF0) | (1 << INTF1)); // Clear INT1 and INT0 interrupt flags
  // -- TIMER 1 SETUP --
  TCCR1A = 0; TCCR1B = 0; // Clear TIMER 1 control registers
  TCNT1 = 0;  // Clear TIMER 1 count register
  TCCR1B |= 0b00000101; // Set prescaler to 1024
  TIMSK1 |= (1 << TOIE1); // Enable TIMER 1 overflow interrupt
  sei();
  // -- INITIALIZE LCD_DISPLAY --
  send_data(0, 0b00000010);   // 4 bit mode 0b00100000 swapped nibbles to work with second set in 8 bit mode
  send_data(0, 0b00101000);   // 4 bit mode and 2 line mode 0b00101000
  send_data(0, 0b00101000);   // 4 bit mode and 2 line mode 0b00101000
  send_data(0, 0b00000001);   // Clear display 0b00000001
  send_data(0, 0b00000010);   // Return home 0b00000010
  send_data(0, 0b00001100);   // Display ON, no cursor 0b00001100
  // -- INITIAL MESSAGE --
  _delay_ms(500);
  set_cursor(0,1);
  print_string("ABB PMU Display");
  set_cursor(2,1);
  print_string("Pace - Pasquarosa");
  set_cursor(3,1);
  print_string("Leoni - Curti");
  _delay_ms(2000);
  send_data(0, 0b00000001);   // Clear display 0b00000001
  send_data(0, 0b00000010);   // Return home 0b00000010
  print_string(" Potenza");

  while (true) {
    // // --- LOOP --- // //
    PINC = 0b10000000;  // Toggle LED_BUILDIN
    for (int i = 0; i < 2; i++) {
      // Power calculation
      if (no_signal_time_count[i] > 16) {
        // No signal, any signals changes detected
        snprintf(buffer, sizeof(buffer), " %s NO_SIGNAL ", labels[i]);
        set_cursor(i+1,0);
        print_string(buffer);
      } else {
        if (differences[i] >= 65535) {
          // Invalid Power value, impulse period > 4.1 s
          snprintf(buffer, sizeof(buffer), " %s <0.86 %s", labels[i], units[i]);
          set_cursor(i+1,0);
          print_string(buffer);
        } else {
          // Valid Power value
          times[i] = (float(differences[i])*64.0e-6) - 9.9e-3;
          powers[i] = 3.6 / times[i];
          if (powers[i] < 0) powers[i] = 0;
          dtostrf(powers[i], 5, 2, float_buffer);
          snprintf(buffer, sizeof(buffer), " %s %s %s", labels[i], float_buffer, units[i]);
          set_cursor(i+1,0);
          print_string(buffer);
        }
      }
    }
    _delay_ms(50);
  }
}

// INT0 interrupt vector
ISR(INT0_vect) {
  if(!captured_flag_INT0) {
    capture_value_INT0 = TCNT1;
    captured_flag_INT0 = true;
  } else {
    if (overflow_flag_INT0 && (TCNT1 >= capture_value_INT0)) {
      differences[0] = 65535;   // MAX valid time value to identify invalid count
    } else {
      differences[0] = TCNT1 - capture_value_INT0;
    }
    overflow_flag_INT0 = false;
    capture_value_INT0 = 0;
    captured_flag_INT0 = false;
    no_signal_time_count[0] = 0;
  }
  EIFR &= ~(1 << INTF0);
}

// INT1 interrupt vector
ISR(INT1_vect) {
   if(!captured_flag_INT1) {
    capture_value_INT1 = TCNT1;
    captured_flag_INT1 = true;
  } else {
    if (overflow_flag_INT1 && (TCNT1 >= capture_value_INT1)) {
      differences[1] = 65535;   // MAX valid time value to identify invalid count
    } else {
      differences[1] = TCNT1 - capture_value_INT1;
    }
    overflow_flag_INT1 = false;
    capture_value_INT1 = 0;
    captured_flag_INT1 = false;
    no_signal_time_count[1] = 0;
  }
  EIFR &= ~(1 << INTF1);
}

// TIMER 1 overflow interrupt vector
ISR(TIMER1_OVF_vect) {
  if(captured_flag_INT0) overflow_flag_INT0 = true;
  if(captured_flag_INT1) overflow_flag_INT1 = true;
  if(!(no_signal_time_count[0] > 16)) no_signal_time_count[0]++;
  if(!(no_signal_time_count[1] > 16)) no_signal_time_count[1]++;
}