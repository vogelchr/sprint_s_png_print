#!/usr/bin/python
from pathlib import Path
import PIL.ImageFont
import PIL.Image
import PIL.ImageDraw
from PIL.BdfFontFile import BdfFontFile
from PIL.PcfFontFile import PcfFontFile
from gzip import GzipFile
import itertools
import argparse
from tempfile import NamedTemporaryFile

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--font', type=str)
args = parser.parse_args()

img = PIL.Image.new('1', (384, 1024), color='white')
draw = PIL.ImageDraw.Draw(img)

y = 0

for fn in Path('fonts').glob('*.pil') :
    if '-' in fn.stem :
        continue
    font = PIL.ImageFont.load(fn)
    s = f'Hello World! {fn}'
    _, _, w, h = font.getbbox(s)
    print(fn, w, h)
    draw.text((0,y), s, font=font)
    y += h

    if y >= 1024 :
        break

img.save('output.png')