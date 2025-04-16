# Xbox-360-chatpad
These python files are made to be used on a raspberry pi pico or similar and enable you to use an xbox 360 chatpad as a keyboard (not fully finished)
there will be 3 files:

1 just displays the output                                   (hexr.py)

2 filters down to just the hex relating to user input        (hexf.py)

3 translates the hex into unicode (when complete)            (chatpad.py) 

the way i have this set up is the rx,tx,ground and 3v  pins of the chatpad being fed into a pico:
rx(chp) -> tx(pico) GPIO-00
tx(chp) -> rx(pico) GPIO-01
ground -> ground
3V -> 3V3(pico (out))
