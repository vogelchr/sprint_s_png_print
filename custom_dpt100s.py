#!/usr/bin/python
import sys
import argparse
import serial
from pathlib import Path
import time
import os
import PIL.Image

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=Path, default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baud', type=int, default=9600)
    parser.add_argument('image', type=Path)
    args = parser.parse_args()

    img = PIL.Image.open(args.image)

    if img.mode != '1' :
        img = img.convert('1')

    assert img.mode == '1'
    assert img.size[0] == 384

    tty = serial.Serial(args.port.as_posix(), args.baud)

    cmd = bytearray(50)
    cmd[0] = 27 # ESC
    cmd[1] = 87 # W


    for y in range(img.size[1]) :
        for x in range(0, img.size[0], 8) :
            c = 0
            for dx in range(8) :
                c = c << 1
                if not img.getpixel((x+dx, y)) :
                    c |= 1
            cmd[2+x//8] = c

        tty.write(cmd)
            
