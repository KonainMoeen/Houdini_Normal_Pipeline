import hou
import random

class HoudiniSetup():
    def __init__(self, args):
        self._render_path = args['output_dir']
        self._render_fileformat = args['render_fileformat']
        self._mask_nodes_to_disable = []
 
    # sets the path of input files in normal composite hip file
    def _setup_composite_input_files(self):
        hou.node('obj/cop2net1/bg').parm('filename1').set(self._render_path + 'Normal_Background.' + self._render_fileformat)
        if 'moss' not in self._mask_nodes_to_disable:
            hou.node('obj/cop2net1/moss').parm('filename1').set(self._render_path + 'Normal_Moss.' +  self._render_fileformat)
        if 'white_lichen' not in self._mask_nodes_to_disable:
            hou.node('obj/cop2net1/white_lichen').parm('filename1').set(self._render_path + 'Normal_WhiteLichen.' +  self._render_fileformat)
        if 'green_lichen' not in self._mask_nodes_to_disable:
            hou.node('obj/cop2net1/green_lichen').parm('filename1').set(self._render_path + 'Normal_GreenLichen.'  + self._render_fileformat)
        
    # To setup masks in the obj context
    def _setup_masks(self, masks_list):
        for mask in masks_list:
            if 'moss' in mask.split('\\')[-1]:
                hou.parm('/obj/main/moss/file').set(mask)
            elif 'green_lichen' in mask.split('\\')[-1]:
                hou.node('/obj/main/green_lichen').parm('file').set(mask)
            elif 'white_lichen' in mask.split('\\')[-1]:
                hou.node('/obj/main/white_lichen').parm('file').set(mask)     
        
    # To setup background maps in materials
    def _setup_background_maps(self,background_maps):
        for map in background_maps:
            if "albedo" in map.split('\\')[-1]:
                hou.node('/obj/lopnet1/albedo_materials/bg_surface_albedo/mtlxUsdUVTexture1').parm('file').set(map)
            elif "normal" in map.split('\\')[-1]:
                hou.node('/obj/lopnet1/normal_materials/bg_surface_normal/mtlxUsdUVTexture2').parm('file').set(map)   
        
    # To setup foreground maps/ classes in materials
    def _setup_forground_maps(self, masks_list, all_maps_dict):
        for selected_mask in masks_list:
            mask_id = selected_mask.split('_')[0]
            
            for map in all_maps_dict['albedo']:
                if map.split('\\')[-1].split('_')[0] ==  mask_id:
                    if 'moss' in selected_mask:
                        hou.node('/obj/lopnet1/albedo_materials/moss_albedo/mtlxUsdUVTexture1').parm('file').set(map)
                    elif 'green_lichen' in selected_mask:
                        hou.node('/obj/lopnet1/albedo_materials/green_lichen_albedo/mtlxUsdUVTexture1').parm('file').set(map)
                    elif 'white_lichen' in selected_mask:
                        hou.node('/obj/lopnet1/albedo_materials/white_lichen_albedo/mtlxUsdUVTexture1').parm('file').set(map)
                        
            for map in all_maps_dict['normal']:
                if map.split('\\')[-1].split('_')[0] ==  mask_id:
                    if 'moss' in selected_mask:
                        hou.node('/obj/lopnet1/normal_materials/moss_normal/mtlxUsdUVTexture2').parm('file').set(map)
                    elif 'green_lichen' in selected_mask:
                        hou.node('/obj/lopnet1/normal_materials/green_lichen_normal/mtlxUsdUVTexture2').parm('file').set(map)
                    elif 'white_lichen' in selected_mask:
                        hou.node('/obj/lopnet1/normal_materials/white_lichen_normal/mtlxUsdUVTexture2').parm('file').set(map)

    # sets the path of main renders 
    def _set__render_path(self):
        hou.parm('/obj/lopnet1/karmarendersettings2/picture').set(self._render_path + 'Mask_GreenLichen.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings3/picture').set(self._render_path + 'Mask_WhiteLichen.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings4/picture').set(self._render_path + 'Mask_Moss.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings/picture').set(self._render_path + 'Albedo.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings1/picture').set(self._render_path + 'Normal_Background.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings5/picture').set(self._render_path + 'Normal_GreenLichen.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings6/picture').set(self._render_path + 'Normal_WhiteLichen.' + self._render_fileformat)
        hou.parm('/obj/lopnet1/karmarendersettings7/picture').set(self._render_path + 'Normal_Moss.' + self._render_fileformat)

    def _set_composite__render_path(self):
        hou.parm('obj/cop2net1/normal_out/copoutput').set(self._render_path + "Normal." + self._render_fileformat)
        
    def _setup_disable_extra_nodes(self, all_maps_dict):
        if not all_maps_dict['moss']: self._mask_nodes_to_disable.append('moss')
        if not all_maps_dict['white_lichen']: self._mask_nodes_to_disable.append('white_lichen')
        if not all_maps_dict['green_lichen']: self._mask_nodes_to_disable.append('green_lichen')
        
    # loads hip file for our script
    def load_hipfile(self, filename):
        try:
            hou.hipFile.load(filename)
        except hou.LoadWarning as e:
            print(e)
            
    # sets the path of input files in main hip file
    def set_input_files(self, background_maps, masks_list, all_maps_dict, index):
        
        self._render_path += '/' + background_maps[1].split('\\')[-1].split('_')[0]  + '/' +  str(index + 1) + '/'

        self._setup_masks(masks_list)
        self._setup_background_maps(background_maps)
        self._setup_forground_maps(masks_list, all_maps_dict)
        self._setup_disable_extra_nodes(all_maps_dict)
        
    # disable render nodes that won't be needed
    def disable_extra_render_nodes(self):
        nodes = []
        for mask in self._mask_nodes_to_disable:
            if mask == 'moss':
                nodes.append('/obj/lopnet1/moss')
                nodes.append('/out/moss_normal')
                nodes.append('/out/moss_mask')
                    
            if mask == 'green_lichen':
                nodes.append('/obj/lopnet1/green_lichen')
                nodes.append('/out/green_lichen_normal')
                nodes.append('/out/green_lichen_mask')
                
            if mask == 'white_lichen':
                nodes.append('/obj/lopnet1/white_lichen')
                nodes.append('/out/white_lichen_normal')
                nodes.append('/out/white_lichen_mask')
                
        for node in nodes:
            hou.node(node).bypass(1)
            
    # disable composite nodes that won't be needed
    def disable_extra_composite_nodes(self):
        for mask in self._mask_nodes_to_disable:
            hou.node('/obj/cop2net1/' + mask).bypass(1)

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
        hou.node('/obj/cop2net1/normal_out').render(verbose=True, output_progress=True)
        
    # save the hip file with increment
    def save_and_increment_hip_file(self):
        hou.hipFile.saveAndIncrementFileName()
        