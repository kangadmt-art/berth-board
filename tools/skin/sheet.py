# usage: python3 sheet.py <full.png> <outPrefix> [sliceH] [perSheet] — cut a tall screenshot into side-by-side slices
import sys
from PIL import Image
src,out=sys.argv[1],sys.argv[2]; H=int(sys.argv[3]) if len(sys.argv)>3 else 1500; N=int(sys.argv[4]) if len(sys.argv)>4 else 5
im=Image.open(src).convert('RGB'); w,h=im.size; sl=[im.crop((0,y,w,min(h,y+H))) for y in range(0,h,H)]
k=0
for i in range(0,len(sl),N):
    grp=sl[i:i+N]; m=Image.new('RGB',((w+8)*len(grp),H),(90,90,90))
    for j,s in enumerate(grp): m.paste(s,(j*(w+8),0))
    k+=1; m.save(f'{out}_{k}.png')
print(src,im.size,'sheets',k)
