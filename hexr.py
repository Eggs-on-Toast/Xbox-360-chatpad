from machine import UART, Pin
import time

uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))

INIT_MESSAGE = bytes([0x87, 0x02, 0x8C, 0x1F, 0xCC])
AWAKE_MESSAGE = bytes([0x87, 0x02, 0x8C, 0x1B, 0xD0])

def send_awake():
    uart.write(AWAKE_MESSAGE)

def initialize_chatpad():
    uart.write(INIT_MESSAGE)
    time.sleep(0.1)
    uart.write(AWAKE_MESSAGE)
    time.sleep(0.1)

print("Initializing Chatpad...")
initialize_chatpad()
last_awake = time.ticks_ms()

print("Chatpad initialized. Waiting for input...")

buffer = bytearray()

while True:
    # Keep Chatpad awake
    if time.ticks_diff(time.ticks_ms(), last_awake) > 500:
        send_awake()
        last_awake = time.ticks_ms()
    # Read incoming bytes
    while uart.any():
        buffer.append(uart.read(1)[0])
        # Only process when we have a full 8-byte message
        if len(buffer) == 8:
            if buffer[0] in (0xA5, 0xB4):
                print(' '.join(f'{b:02X}' for b in buffer))
            buffer = bytearray()
    time.sleep(0.01)
