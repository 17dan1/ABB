/*
 * Simulatore Uscita Impulsi Energia Reattiva  ABB_PMU
 * Created: 19/03/2026
 * Author : Emanuele Pace
 * Featuring : logic2_bin_to_arduino_sim.py
 * Note: Pure C coding is better :)
 */ 

#define INITIAL_STATE 1
#define SAMPLES 118
unsigned long timing[] = {418068, 9926, 1081450, 8901, 1082935, 9930, 1083510, 9928, 1080174, 9926, 1081641, 9930, 1082936, 9930, 1083877, 9929, 1083005, 9924, 1081838, 9934, 1081839, 9933, 1085999, 9930, 1084877, 9929, 1082871, 9932, 1082839, 9932, 1083088, 9934, 1083873, 9933, 1086821, 9994, 1087745, 9931, 1088972, 9932, 1085905, 9939, 1083871, 9930, 1086060, 9930, 1085907, 9931, 1085907, 9931, 1087065, 9932, 1084903, 9931, 1084970, 9929, 1087941, 9931, 1087937, 9932, 1089032, 9932, 1084874, 9933, 1084902, 9933, 1082842, 9931, 1083968, 8899, 1084905, 8898, 1083974, 9924, 1083879, 9924, 1081842, 9929, 1080965, 9931, 1078803, 9939, 1079802, 9929, 1082934, 8900, 1082873, 9930, 1078774, 9933, 1078809, 9928, 1081843, 9932, 1080899, 8898, 1080840, 9932, 1079810, 9929, 1083873, 9931, 1081842, 9933, 1080900, 9931, 1079809, 9928, 1082842, 9931, 1081932, 8901, 1082870, 9931, 1079808, 9930, 1080902, 9970};

// Assembly compiler instruction clock delay
void __attribute__((noinline)) delay_us(unsigned long value) {
  unsigned long count = value * 1.44345;   //2.64637 clean 500ms
  for (long i = 0; i < count; i++) {
    asm("");
  }
}

int main() {
  // Initialize digital pin  13, PB5 as output
  DDRB = (1 << PB5);
  // Set initial state
  if (!INITIAL_STATE) {
    PORTB = (1 << PB5);
  }
  while (true) {
    // Infinite loop to scroll the timing vector and toggle the pin status
    for (int i=0; i<SAMPLES; i++) {
      PINB = (1 << PB5);
      delay_us(timing[i]);
    }
  }
}
