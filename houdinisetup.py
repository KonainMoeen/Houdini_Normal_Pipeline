import hou
import random
import os
import cv2
import numpy as np
from PIL import Image


class HoudiniSetup():
    def __init__(self, args):
        self.args = args
        self._render_fileformat = self.args['render_fileformat']
        self._mask_nodes_to_disable = []
        
    def _set_output_folder(self, batch_number, background_map_id, index):        
        self._render_path = self.args['output_dir'] + '/' +  'batch' + str(batch_number + 1) + '/' + background_map_id.split('\\')[-1].split('_')[0]  + '/' +  str(index + 1) + '/'
        
        
    # sets the path of input files in normal composite hip file
    
    def _setup_composite_input_files(self):
        hou.node('obj/Composite/bg').parm('filename1').set(self._render_path + 'Normal_Background.' + self._render_fileformat)
        if 'moss' not in self._mask_nodes_to_disable:
            hou.node('obj/Composite/moss').parm('filename1').set(self._render_path + 'Normal_Moss.' +  self._render_fileformat)
        if 'white_lichen' not in self._mask_nodes_to_disable:
            hou.node('obj/Composite/white_lichen').parm('filename1').set(self._render_path + 'Normal_WhiteLichen.' +  self._render_fileformat)
        if 'green_lichen' not in self._mask_nodes_to_disable:
            hou.node('obj/Composite/green_lichen').parm('filename1').set(self._render_path + 'Normal_GreenLichen.'  + self._render_fileformat)
        
    # To setup masks in the obj context
    def _setup_masks(self, masks_list):
        for mask in masks_list:
            if 'moss' in mask.split('\\')[-1]:
                hou.parm('/obj/Geometry/moss/file').set(mask)
            elif 'green_lichen' in mask.split('\\')[-1]:
                hou.node('/obj/Geometry/green_lichen').parm('file').set(mask)
            elif 'white_lichen' in mask.split('\\')[-1]:
                hou.node('/obj/Geometry/white_lichen').parm('file').set(mask)     
        
    # To setup background maps in materials
    def _setup_background_maps(self,background_maps):
        for map in background_maps:
            if "albedo" in map.split('\\')[-1]:
                hou.node('/obj/Render/albedo_materials/bg_surface_albedo/mtlxUsdUVTexture1').parm('file').set(map)
            elif "normal" in map.split('\\')[-1]:
                hou.node('/obj/Render/normal_materials/bg_surface_normal/mtlxUsdUVTexture2').parm('file').set(map)   
        
    # To setup foreground maps/ classes in materials
    def _setup_forground_maps(self, masks_list, all_maps_dict):
        for selected_mask in masks_list:
            mask_id = selected_mask.split('_')[0]
            
            for map in all_maps_dict['albedo']:
                if map.split('\\')[-1].split('_')[0] ==  mask_id:
                    if 'moss' in selected_mask:
                        hou.node('/obj/Render/albedo_materials/moss_albedo/mtlxUsdUVTexture1').parm('file').set(map)
                    elif 'green_lichen' in selected_mask:
                        hou.node('/obj/Render/albedo_materials/green_lichen_albedo/mtlxUsdUVTexture1').parm('file').set(map)
                    elif 'white_lichen' in selected_mask:
                        hou.node('/obj/Render/albedo_materials/white_lichen_albedo/mtlxUsdUVTexture1').parm('file').set(map)
                        
            for map in all_maps_dict['normal']:
                if map.split('\\')[-1].split('_')[0] ==  mask_id:
                    if 'moss' in selected_mask:
                        hou.node('/obj/Render/normal_materials/moss_normal/mtlxUsdUVTexture2').parm('file').set(map)
                    elif 'green_lichen' in selected_mask:
                        hou.node('/obj/Render/normal_materials/green_lichen_normal/mtlxUsdUVTexture2').parm('file').set(map)
                    elif 'white_lichen' in selected_mask:
                        hou.node('/obj/Render/normal_materials/white_lichen_normal/mtlxUsdUVTexture2').parm('file').set(map)

    # sets the path of Geometry renders 
    def _set__render_path(self):
        hou.parm('/obj/Render/karmarendersettings2/picture').set(self._render_path + 'Mask_GreenLichen.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings3/picture').set(self._render_path + 'Mask_WhiteLichen.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings4/picture').set(self._render_path + 'Mask_Moss.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings/picture').set(self._render_path + 'Albedo.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings1/picture').set(self._render_path + 'Normal_Background.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings5/picture').set(self._render_path + 'Normal_GreenLichen.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings6/picture').set(self._render_path + 'Normal_WhiteLichen.' + self._render_fileformat)
        hou.parm('/obj/Render/karmarendersettings7/picture').set(self._render_path + 'Normal_Moss.' + self._render_fileformat)

    def _set_composite__render_path(self):
        hou.parm('obj/Composite/normal_out/copoutput').set(self._render_path + "Normal." + self._render_fileformat)
        
    def _setup_disable_extra_nodes(self, all_maps_dict):
        if not all_maps_dict['moss']: self._mask_nodes_to_disable.append('moss')
        if not all_maps_dict['white_lichen']: self._mask_nodes_to_disable.append('white_lichen')
        if not all_maps_dict['green_lichen']: self._mask_nodes_to_disable.append('green_lichen')
        
        self._disable_extra_render_nodes()
        self._disable_extra_composite_nodes()
        
    def _set_render_resolution(self):
        hou.parmTuple('obj/Render/karmarendersettings/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings1/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings2/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings3/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings4/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings5/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings6/resolution').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Render/karmarendersettings7/resolution').set((self.args['image_res'], self.args['image_res']))

    
    def _set_composite_resolution(self):
        hou.parmTuple('obj/Composite/bg/size').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Composite/moss/size').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Composite/white_lichen/size').set((self.args['image_res'], self.args['image_res']))
        hou.parmTuple('obj/Composite/green_lichen/size').set((self.args['image_res'], self.args['image_res']))

        
    # disable render nodes that won't be needed
    def _disable_extra_render_nodes(self):
        nodes = []
        for mask in self._mask_nodes_to_disable:
            if mask == 'moss':
                nodes.append('/obj/Render/moss')
                nodes.append('/out/moss_normal')
                nodes.append('/out/moss_mask')
                    
            if mask == 'green_lichen':
                nodes.append('/obj/Render/green_lichen')
                nodes.append('/out/green_lichen_normal')
                nodes.append('/out/green_lichen_mask')
                
            if mask == 'white_lichen':
                nodes.append('/obj/Render/white_lichen')
                nodes.append('/out/white_lichen_normal')
                nodes.append('/out/white_lichen_mask')
                
        for node in nodes:
            hou.node(node).bypass(1)
            
    # disable composite nodes that won't be needed
    def _disable_extra_composite_nodes(self):
        for mask in self._mask_nodes_to_disable:
            hou.node('/obj/Composite/' + mask).bypass(1)
        
    # loads hip file for our script
    def load_hipfile(self, filename):
        try:
            hou.hipFile.load(filename)
        except hou.LoadWarning as e:
            print(e)
            
    # sets the path of input files in Geometry hip file
    def set_houdini(self, batch_number, background_maps, index, masks_list, all_maps_dict):
        
        self._set_output_folder(batch_number, background_maps[1], index)
        self._setup_masks(masks_list)
        self._setup_background_maps(background_maps)
        self._setup_forground_maps(masks_list, all_maps_dict)
        self._setup_disable_extra_nodes(all_maps_dict)
        self._set_render_resolution()
        self._set_composite_resolution()
        
    # set frame number as random unless a frame number is given
    def setFrameNumber(self,frame):
        if frame:
            hou.setFrame(frame)
        else:
            hou.setFrame(random.randint(0,240))
    
    #renders the image from lops-karma
    def render(self):
        self._set__render_path()
        hou.node('/out/render_all').render(verbose=True, output_progress=True)
    
    #renders the composited image
    def render_composite(self):
        self._setup_composite_input_files()
        self._set_composite__render_path()
        hou.node('/obj/Composite/normal_out').render(verbose=True, output_progress=True)
        
    # save the hip file with increment
    def save_and_increment_hip_file(self):
        hou.hipFile.saveAndIncrementFileName()
        
        
    def preprocess_3D_asset_masks(self,args):
            
        # loading UV_baking.hip
        try:
            hou.hipFile.load(args['UV_baking_hipfile'])
        except hou.LoadWarning as e:
            print(e)
        # set resolution for unwrapping, takes around 3min for 1 3d-asset. Could possibly be optimized. Currently renders with CPU only.
        resolution = args['UV_baking_resoluton']
        resolution_str = str(int(resolution / 1024))
        hou.node("/out/baketexture").parm("vm_uvunwrapresx").set(resolution)
        hou.node("/out/baketexture").parm("vm_uvunwrapresy").set(resolution)
        #  initilize variables for current example
        masked_3d_dir = args['masked_3d_dir']
        temp_UV_baking_folder = args['UV_baking_temp_dir']
        # start looping through every masked_3d_asset, import fbx and bake UV-islands when needed.
        for asset_id in os.listdir(masked_3d_dir):
            asset_folder = masked_3d_dir + '/' + asset_id
            fbx_file, uv_found, uv_mask, surfacemasks = "", False, None, {}
            for f in os.listdir(asset_folder):
                fn = asset_folder + '/' + f
                if f.endswith('.fbx'):
                    fbx_file = fn
                if 'surfacemask' in f.lower():
                    print(asset_id)
                    c = f.lower().split('surfacemask_')[1].split('.')[0]
                    surfacemasks[c] = fn
                if 'UV-islands' in f:
                    uv_found = True
                    uv_mask = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
            surfacemasks_fn = {c: fn for c, fn in surfacemasks.items() if 'UV-filtered' not in os.path.basename(fn)}
            if not surfacemasks_fn: continue
            uv_mask_filename = os.path.join(asset_folder, asset_id+'_'+resolution_str+'K'+'_UV-islands.png')
            if not uv_found:
                # Check if files exists, raise exception otherwise.
                if not fbx_file:
                    raise Exception(asset_folder + ": does not contain a fbx file!")
            
                # import and bake the fbx file
                hou.node("/out/baketexture").parm("vm_uvoutputpicture1").set(temp_UV_baking_folder + '/' + asset_id)
                hou.node("/obj/subnet1/geo1/file1").parm('file').set(fbx_file)
                hou.node("/out/baketexture").render(verbose=True, output_progress=True)
                
                # Use the mask for UV-islands temporarily created by baking the texture and create a filtered mask.
                for f in os.listdir(temp_UV_baking_folder):
                    fn = os.path.join(temp_UV_baking_folder, f)
                    if 'basecolor' in f:
                        uv_mask = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
                        _, uv_mask = cv2.threshold(uv_mask[:, :, 3], 0, 255, cv2.THRESH_BINARY)
                        uv_mask = cv2.cvtColor(uv_mask, cv2.COLOR_RGBA2RGB)
                        cv2.imwrite(uv_mask_filename, uv_mask)
                        os.remove(fn)
                    else:
                        os.remove(fn)
            
            for mask_class, unfiltered_mask_fn in surfacemasks_fn.items():
                uv_mask = cv2.imread(uv_mask_filename)
                unfiltered_mask = np.array(Image.open(unfiltered_mask_fn).convert('RGB'))
                unfiltered_mask[uv_mask == 0] = 0
                cv2.imwrite(os.path.join(asset_folder, asset_id + '_' + resolution_str + 'K_UV-filtered_surfacemask_'+ mask_class +'.png'), unfiltered_mask)
                os.remove(unfiltered_mask_fn)