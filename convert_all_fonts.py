#!/usr/bin/python
from pathlib import Path
import PIL.ImageFont
import PIL.Image
import PIL.ImageDraw
from PIL.BdfFontFile import BdfFontFile
from PIL.PcfFontFile import PcfFontFile
from gzip import GzipFile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('src_path', type=Path)
parser.add_argument('dest_path', type=Path)
args = parser.parse_args()

for fn in args.src_path.glob('*'):

    if '.pcf' in fn.suffixes:
        cls = PcfFontFile
    elif '.bdf' in fn.suffixes:
        cls = BdfFontFile
    else:
        print(f'Skipping {fn}...')
        continue

    if '.gz' in fn.suffixes:
        # stem only removes the outermost suffix, we assume that's .gz
        fontname = Path(fn.stem).stem
        fp = GzipFile(fn)
    else:
        fontname = fn.stem
        fp = fn.open('rb')

    print(f'Converting {fontname}...')
    try:
        pff = cls(fp)
        pff.compile()
        pff.save(args.dest_path / fontname)
    except Exception as exc:
        print('Exception', repr(exc), 'raised during conversion!')
