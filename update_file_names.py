import os, re

path = "C:/users/Administrator/Documents/Dynamic_Houdini_Pipeline/assets"
surfacemask_channel = re.compile('surfacemask[|r|g|b]')

updated_filename = ""

for root,dir,files in os.walk(path):
    for filename in files:
        if 'surfacemask' in filename:
            updated_filename = re.sub(surfacemask_channel, 'surfacemask', filename)
            if "green lichen" in filename:
                updated_filename = updated_filename.replace('green lichen', 'green_lichen')
            if "white lichen" in filename:
                updated_filename = updated_filename.replace('white lichen', 'white_lichen')            
            os.rename(os.path.join(root, filename).replace('\\', '/'), os.path.join(root, updated_filename).replace('\\', '/'))

