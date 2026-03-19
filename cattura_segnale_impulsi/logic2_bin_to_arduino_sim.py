# * Python Saleae .bin digital parser to arduino simulation data
# * Created: 19/03/2026
# * Author : Emanuele Pace
# * Featuring : https://www.saleae.com/support/logic-software/saving-and-exporting-data/binary-and-csv-export-formats-2025-update

# ARDUINO SCRIPT
"""
/*
 * Simulatore Uscita Impulsi da cattura .bin  Saleae Logic2
 * Created: 19/03/2026
 * Author : Emanuele Pace
 * Featuring : logic2_bin_to_arduino_sim.py
 * Note: Pure C coding is better :)
 */ 

#define INITIAL_STATE ...
#define SAMPLES ...
long timing[] = ...

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

// Assembly compiler instruction clock delay
void delay_us(long value) {
  long count = value * 1.323;   //2.64637 clean 500ms
  for (long i = 0; i < count; i++) {
    asm("");
  }
}
"""

import struct
import sys
from dataclasses import dataclass
from typing import List, BinaryIO, Optional

# Constants
TYPE_DIGITAL = 0
TYPE_ANALOG = 1

@dataclass
class DigitalChunk:
    """Represents a continuous segment of digital data"""
    initial_state: int  # 0 = Low, 1 = High
    sample_rate: Optional[float]  # Samples per second (None for version 0)
    begin_time: float  # Start time in seconds
    end_time: float  # End time in seconds
    num_transitions: int  # Number of state changes
    transition_times: List[float]  # Times when state changes occur

@dataclass
class DigitalData:
    """Complete digital data export containing one or more chunks"""
    chunks: List[DigitalChunk]

def parse_digital_v1(f: BinaryIO) -> DigitalData:
    """Parse Logic 2 digital binary format version 1"""

    # Parse header
    identifier = f.read(8)
    if identifier != b"<SALEAE>":
        raise ValueError("Not a Saleae file")

    version, datatype = struct.unpack('<ii', f.read(8))

    if datatype != TYPE_DIGITAL:
        raise ValueError(f"Expected digital data, got type {datatype}")

    if version not in [0, 1]:
        raise ValueError(f"Unsupported version: {version}")

    chunks = []

    if version == 0:
        # Version 1 format - single chunk without chunk count
        chunk_count = 1
    else:
        # Version 1 format
        chunk_count, = struct.unpack('<Q', f.read(8))

    for _ in range(chunk_count):
        # Parse chunk header
        initial_state, = struct.unpack('<I', f.read(4))

        if version >= 1:
            sample_rate, = struct.unpack('<d', f.read(8))
        else:
            sample_rate = None

        begin_time, end_time, num_transitions = struct.unpack('<ddQ', f.read(24))

        # Parse transition times
        transition_times = []
        for _ in range(num_transitions):
            time, = struct.unpack('<d', f.read(8))
            transition_times.append(time)

        chunks.append(DigitalChunk(
            initial_state=initial_state,
            sample_rate=sample_rate,
            begin_time=begin_time,
            end_time=end_time,
            num_transitions=num_transitions,
            transition_times=transition_times
        ))

    return DigitalData(chunks=chunks)

def print_digital_data(data: DigitalData):
    """Print digital data in human readable format"""
    print(f"Digital data with {len(data.chunks)} chunk(s)")

    for i, chunk in enumerate(data.chunks):
        print(f"\n--- Chunk {i} ---")
        initial_state_str = 'Low' if chunk.initial_state == 0 else 'High'
        print(f"Initial state: {initial_state_str}")
        if chunk.sample_rate:
            print(f"Sample rate: {chunk.sample_rate} Hz")
        print(f"Time range: {chunk.begin_time:.6f}s to {chunk.end_time:.6f}s")
        print(f"Transitions: {chunk.num_transitions}")
        """Code modified for Arduino Configuration"""
        print("")
        print("ARDUINO CONFIGURATION:")
        print("")
        # Print Initial status and samples number
        print(f"#define INITIAL_STATE {chunk.initial_state}")
        print(f"#define SAMPLES {chunk.num_transitions}")
        # Show state changes
        first_diff = chunk.transition_times[0] *1000000
        print("long timing[] = {", end="")
        print(f"{first_diff:>.0f}", end="")
        for current, next_t in zip(chunk.transition_times, chunk.transition_times[1:]):
            diff = next_t - current
            diff = diff*1000000;
            print(f", {diff:>.0f}", end="")
        print(" };", end="")

# Usage example
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python parse_digital.py <digital_file.bin>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        data = parse_digital_v1(f)

    print_digital_data(data)