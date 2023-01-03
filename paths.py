import argparse
import sys

def get_json_file():
    return "configuration.json"

def append_anaconda3_library():
    sys.path.append("c:/users/Konain/anaconda3/lib/site-packages")

def get_houdini_path():
   houdini_path = "D:/Softwares/Side Effects Software/Houdini 19.5.368/"
   return houdini_path


def get_parser():
    parser = argparse.ArgumentParser(
        prog='syntheticDataGeneration',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--hipfile', 
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/Pipeline/HoudiniNormalPipeline.hip',
                        help='filename/path for the main .hip file')
    
    parser.add_argument('--comphipfile', 
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/Pipeline/Normal Composite.hip',
                        help='filename/path for the composite .hip file')

    parser.add_argument('--HIP', 
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/pipeline',
                        help='equivalent to $HIP path in the .hip file')

    parser.add_argument('--background_surfaces_dir',
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/assets/surface/rock',
                        help='path to the folder containing the surface assets to use as background')

    parser.add_argument('--masked_3d_dir',
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/assets/masked_3d',
                        help='path to the folder containing the asset folders that have masked 3d assets.')

    parser.add_argument('--masked_surfaces_dir',
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/assets/masked_surfaces',
                        help='path to the folder containing the asset folders that have masked surfaces.')

    parser.add_argument('--atlas_decal_dir',
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/assets/atlas_decal',
                        help='path to the folder containing the asset folders that have atlases and decals.')

    parser.add_argument('--image_res_div', 
                        default=8,
                        help='to calculate reolution for each render, 8192 / image_res_div = resolution')

    parser.add_argument('--render_fileformat', 
                        default='exr',
                        help='the fileformat to render albedo and mask in')

    parser.add_argument('--output_dir', 
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/renders/test',
                        help='the place where the output files will be placed')

    parser.add_argument('--UV_baking_hipfile',
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/UV_baking/UV_baking.hip',
                        help='path to the hipfile for UV_baking')

    parser.add_argument('--UV_baking_resoluton',
                        default=8192,
                        help='resolution to focus on while preprocessing the 3d assets for UV baking')
                        
    parser.add_argument('--UV_baking_temp_dir',
                        default='C:/Users/Konain/Desktop/Houdini Normal Pipeline/UV_baking/temp',
                        help='path to the a temp folder used while baking the UV-islands')

    return parser