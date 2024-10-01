#!/usr/bin/python
import sys
import argparse
import serial
from pathlib import Path
import time
import os
import PIL.Image


def white_black_lines(tty, n=1, is_black=False):
    cmd = bytearray(50)
    cmd[0] = 27  # ESC
    cmd[1] = 87  # W
    if is_black:
        cmd[2:50] = [255 for i in range(48)]
    tty.write(cmd)


def write_img_line(tty, img, y):
    cmd = bytearray(50)
    cmd[0] = 27  # ESC
    cmd[1] = 87  # W

    # x position and byte position in cmd
    x, b = 0, 2
    c, mask = 0, 0x80

    while x < 384:
        if x < img.size[0] and not img.getpixel((x, y)):
            c |= mask

        mask >>= 1
        x += 1

        # 8 bytes are done
        if not mask:
            cmd[b] = c
            b += 1
            c = 0
            mask = 0x80

    tty.write(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=Path, default='/dev/ttyUSB0',
                        help='Serial port, default: %(default)s')
    parser.add_argument('-b', '--baud', type=int, default=38400,
                        help='Baud rate, default: %(default)d')
    parser.add_argument('-c', '--cut-lines', action='store_true',
                        help='Draw a horizontal line and additional whitespace around the image.')
    parser.add_argument(
        '-s', '--square', action='store_true',
        help='Make square by doubling every 7th line.')
    parser.add_argument('image', type=Path)
    args = parser.parse_args()

    img = PIL.Image.open(args.image)

    if img.mode != '1':
        img = img.convert('1')

    tty = serial.Serial(args.port.as_posix(), args.baud, rtscts=True)

    if args.cut_lines:
        white_black_lines(tty, 20)
        white_black_lines(tty, 1, True)

    for y in range(img.size[1]):
        write_img_line(tty, img, y)
        if args.square and (y % 7 == 0):
            write_img_line(tty, img, y)

    if args.cut_lines:
        white_black_lines(tty, 1, True)
        white_black_lines(tty, 96)
