from PIL import Image,ImageFilter
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im=Image.open(R+'/assets/cover_src.png').convert('RGB')
w,h=im.size;m=min(w,h);im=im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m))
os.makedirs(R+'/assets/icons',exist_ok=True)
for z in(32,64,120,152,167,180,192,512,1024):
    t=im.resize((z,z),Image.LANCZOS)
    if z<=192:t=t.filter(ImageFilter.UnsharpMask(radius=0.8,percent=60,threshold=2))
    t.save(f'{R}/assets/icons/icon-{z}.png',optimize=True)
im.resize((64,64),Image.LANCZOS).save(R+'/assets/icons/favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
print('icons ok',os.listdir(R+'/assets/icons'))
