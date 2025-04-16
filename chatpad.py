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
buffer = bytearray()

main_keymap = {
    0x17: '1',
    0x16: '2',
    0x15: '3',
    0x14: '4',
    0x13: '5',
    0x12: '6',
    0x11: '7',
    0x67: '8',
    0x66: '9',
    0x65: '0',
    0x27: 'q',
    0x26: 'w',
    0x25: 'e',
    0x24: 'r',
    0x23: 't',
    0x22: 'y',
    0x21: 'u',
    0x76: 'i',
    0x75: 'o',
    0x64: 'p',
    0x37: 'a',
    0x36: 's',
    0x35: 'd',
    0x34: 'f',
    0x33: 'g',
    0x32: 'h',
    0x31: 'j',
    0x77: 'k',
    0x72: 'l',
    0x62: ',',
    0x46: 'z',
    0x45: 'x',
    0x44: 'c',
    0x43: 'v',
    0x42: 'b',
    0x41: 'n',
    0x52: 'm',
    0x53: '.',
    0x63: '\n',
    0x55: '',     # Left arrow (blank)
    0x51: '',     # Right arrow (blank)
    0x54: ' ',    # Space
    0x71: '\b',   # Backspace
}

orange_keymap = {
    0x27: '¡',    # q
    0x26: 'å',    # w
    0x25: 'é',    # e
    0x24: '$',    # r
    0x23: 'Þ',    # t
    0x22: 'ý',    # y
    0x21: 'ú',    # u
    0x76: 'í',    # i
    0x75: 'ó',    # o
    0x64: '=',    # p
    0x27: '¡',    # q
    0x26: 'å',    # w
    0x25: 'é',    # e
    0x24: '$',    # r
    0x23: 'Þ',    # t
    0x22: 'ý',    # y
    0x21: 'ú',    # u
    0x76: 'í',    # i
    0x75: 'ó',    # o
    0x64: '=',    # p
    0x37: 'á',    # a
    0x36: 'ß',    # s 
    0x35: 'ð',    # d
    0x34: '£',    # f
    0x33: '¥',    # g
    0x32: '\\',   # h 
    0x31: '"',    # j 
    0x77: '',     # k (Microsoft Points blank)
    0x72: 'Ø',    # l
    0x62: ';',    # , 
    0x46: 'æ',    # z
    0x45: 'œ',    # x
    0x44: 'ç',    # c
    0x43: '_',    # v
    0x42: '+',    # b
    0x41: 'ñ',    # n
    0x52: 'µ',    # m
    0x53: '¿',    # .
#Æ
}

green_keymap = {
    0x27: '!',    # q
    0x26: '@',    # w
    0x25: '€',    # e
    0x24: '#',    # r
    0x23: '%',    # t
    0x22: '^',    # y
    0x21: '&',    # u
    0x76: '*',    # i
    0x75: '(',    # o
    0x64: ')',    # p
    0x37: '~',    # a
    0x36: 'š',    # s
    0x35: '{',    # d
    0x34: '}',    # f
    0x33: '',     # g (blank)
    0x32: '/',    # h
    0x31: "'",    # j
    0x77: '[',    # k
    0x72: ']',    # l
    0x62: ':',    # ,
    0x46: '',     # z (blank)
    0x45: '',     # x (blank)
    0x44: '',     # c (blank)
    0x43: '-',    # v
    0x42: '|',    # b
    0x41: '<',    # n
    0x52: '>',    # m
    0x53: '?',    # .
}

last_key = 0
last_mod = 0

while True:
    if time.ticks_diff(time.ticks_ms(), last_awake) > 500:
        send_awake()
        last_awake = time.ticks_ms()
    while uart.any():
        buffer.append(uart.read(1)[0])
        if len(buffer) == 8:
            if buffer[0] == 0xB4:
                key1 = buffer[4]
                mod = buffer[3]
                if key1 != 0 and (key1 != last_key or mod != last_mod):
                    # Modifier selection logic
                    if mod == 0x04:  # Orange modifier held
                        print(orange_keymap.get(key1, f"Unknown({key1:02X})"), end="")
                    elif mod == 0x02:  # Green modifier held
                        print(green_keymap.get(key1, f"Unknown({key1:02X})"), end="")
                    else:
                        print(main_keymap.get(key1, f"Unknown({key1:02X})"), end="")
                last_key = key1
                last_mod = mod
            buffer = bytearray()
    time.sleep(0.01)

