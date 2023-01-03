import sys
import os, sys
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
from paths import append_anaconda3_library
append_anaconda3_library()
from houdinisetup import HoudiniSetup
import itertools
import cv2
import numpy as np
import shutil 
from PIL import Image
import json
import math
from paths import get_parser, get_json_file
from filestructure import FileStructureSetup

argv = sys.argv[1:]
def main(args = vars(get_parser().parse_known_args(argv)[0])):   
    
    ## read json file
    jsonObj = json.load(open(get_json_file()))
    
    ## setup json variables
    batches = jsonObj['batches']
    # looping through each batch represented per line in batches_to_render.txt
    for batch_idx, current_batch in enumerate(batches):
        
        renders_per_surface = jsonObj['batches'][batch_idx]['min_num_samples']
        if renders_per_surface == 0: continue

        asset_types_3d = jsonObj['batches'][batch_idx]['asset_types']['3D']
        asset_types_surface = jsonObj['batches'][batch_idx]['asset_types']['surface']
        asset_types_atlas = jsonObj['batches'][batch_idx]['asset_types']['atlas']
        intensity_multiplier = jsonObj['batches'][batch_idx]['scatter_percent']
        b_mix_multiple_instances = jsonObj['batches'][batch_idx]['mix_multiple_instances']
        
        # if any(asset_types_3d):
        #     print('Initilize preprocessing UV-islands for 3d-assets')
        #     #preprocess_3D_asset_masks(args)
        #     print('DONE: masks for UV-islands created for all 3d-assets!')
    
        # ## load the hip file
        # houObj = HoudiniSetup("C:/Users/Konain/Desktop/Houdini Normal Pipeline/renders/")
        # houObj.load_hipfile(args['hipfile'])
        
        ## for the select batch setup file structure
        fileObj = FileStructureSetup(asset_types_3d, asset_types_surface, asset_types_atlas)
        fileObj.read_files()
        # for background in fileObj.assetfiles_bg:
             
        # if not b_mix_multiple_instances:
        #     totalcount = (len(fileObj.assetfiles_atlas) if len(fileObj.assetfiles_atlas) > 0  else 1 ) * (len(fileObj.assetfiles_3d) if len(fileObj.assetfiles_3d) > 0  else 1 ) * (len(fileObj.assetfiles_surfaces) if len(fileObj.assetfiles_surfaces) > 0  else 1 )
        # else:
        #     totalcount = renders_per_surface
        totalcount = renders_per_surface
        #for index, renders in enumerate(totalcount):
                
        #print(totalcount)
        print(fileObj.get_maps_set())
        #print(fileObj.assetmaps)
                
        #         # # setup files in Houdini
        #         # houObj.set_input_files(background,fileObj.get_maps_set())
                
        #         # ## render
        #         # houObj.render()
                
        #         # # setup composite
        #         # houObj.load_hipfile(args['comphipfile'])
                
        #         # ## composite
        #         # houObj.render_composite()
                
        #         # houObj.save_and_increment_file()
        
    print("Completed")
    
    
if __name__ == '__main__':
    main()