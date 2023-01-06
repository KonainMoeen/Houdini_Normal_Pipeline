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
from pprint import pprint

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
        
        # Using the json input, read the asset maps and setup the render structure
        fileObj = FileStructureSetup(asset_types_3d, asset_types_surface, asset_types_atlas)
        fileObj.read_files()
        
        for background_maps in fileObj.get_background_maps_list():
            
            if not b_mix_multiple_instances:
                total_count = (len(fileObj.get_all_maps_dict()['green_lichen']) if len(fileObj.get_all_maps_dict()['green_lichen']) > 0  else 1 ) * (len(fileObj.get_all_maps_dict()['white_lichen']) if len(fileObj.get_all_maps_dict()['white_lichen']) > 0  else 1 ) * (len(fileObj.get_all_maps_dict()['moss']) if len(fileObj.get_all_maps_dict()['moss']) > 0  else 1 )
            else:
                total_count = renders_per_surface
                
            for index in range(total_count):
                
                ## print all of the maps read from the assets folder / print the masks for the current render
                #pprint(fileObj.get_all_maps_dict())
                #pprint(fileObj.get_masks_list()[index])
                        
                ## open the main pipeline hip file, set the maps and render 
                houObj = HoudiniSetup(args)
                houObj.load_hipfile(args['hipfile'])
                houObj.set_input_files(background_maps, fileObj.get_masks_list()[index], fileObj.get_all_maps_dict(), index)
                houObj.disable_extra_render_nodes()                
                houObj.setFrameNumber(None)
                houObj.render()
                
                ## open the composite file, blend the background normal map with foreground normals maps of classes and output the normal map in the render folder
                houObj.load_hipfile(args['comphipfile'])
                houObj.disable_extra_composite_nodes()
                houObj.render_composite()
                #houObj.save_and_increment_hip_file()
        
    print("Completed")
    
if __name__ == '__main__':
    main()