import hou
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
import numpy as np
from PIL import Image
import cv2

from New_paths import Paths
from New_settings import Settings



class HoudiniSetup():
    def __init__(self):
        self.paths = Paths()
        self.settings = Settings()
    
    def load_hipfile(self, filename):
        try:
            hou.hipFile.load(filename)
        except hou.LoadWarning as e:
            print(e)
            
    def save_and_increment_hip_file(self):
        hou.hipFile.saveAndIncrementFileName()
        
    def _fix_layout(self,parent_node):
        parent_node.layoutChildren()
    
    def _create_NetworkBox(self, nodes):
        network_box = nodes[0].parent().createNetworkBox()
        for node in nodes:
            network_box.addItem(node)
        network_box.fitAroundContents()
        
            
    
    def _obj_set_references(self):
        
        self.geometry = hou.node('/obj/Geometry')
        
        mask = self.geometry.node('mask_default')
        uv = self.geometry.node('uvproject_default')
        foreach_begin =self.geometry.node('foreach_begin_default')
        delete_small_parts = self.geometry.node('delete_small_parts_default')
        center_position = self.geometry.node('center_position_default')
        foreach_end = self.geometry.node('foreach_end_default')
        group = self.geometry.node('group_default')
        merge = self.geometry.node('merge_default')
        connectivity = self.geometry.node('connectivity_default')
        scatter = self.geometry.node('scatter_default')
        randomize_rotations = self.geometry.node('randomize_rotation_default')
        sort = self.geometry.node('sort_default')
        attribute_from_pieces = self.geometry.node('attribfrompieces_default')
        copytopoints = self.geometry.node('copytopoints_default')
        reverse = self.geometry.node('reverse_default')
        attribdelete  = self.geometry.node('attribdelete_default')
        transform = self.geometry.node('transform_default')
        
        self.default_setup_nodes = (mask, uv, foreach_begin, delete_small_parts, center_position,foreach_end, group, merge,connectivity,scatter,randomize_rotations,sort,attribute_from_pieces,copytopoints, reverse, attribdelete, transform)
        self.extra_setup_nodes = (mask, uv, foreach_begin, delete_small_parts, center_position,foreach_end, group)
        
        
    def _lop_set_references(self):
        
        self.lop = hou.node('/obj/Render')
        #self.lop.createNode('sopimport')

        # for mask
        mask_render_settings = self.lop.node('karmarendersettings_default_mask')
        mask_render = self.lop.node('render_default_mask')
        
        #for albedo
        merge = self.lop.node('merge_all_albedo')
        albedo_material_library = self.lop.node('materiallibrary_all_albedo')
        albedo_render_settings = self.lop.node('karmarendersettings_default_albedo')
        albedo_render = self.lop.node('render_default_albedo')

        # for normal
        normal_material_library = self.lop.node('materiallibrary_default_normal')
        normal_render_settings = self.lop.node('karmarendersettings_default_normal')
        normal_render = self.lop.node('render_default_normal')

        self.lop_mask_nodes = (mask_render, mask_render_settings)
        self.lop_albedo_nodes = (merge, albedo_material_library, albedo_render_settings, albedo_render)
        self.lop_normal_nodes = (normal_material_library, normal_render_settings, normal_render)
            
    def _obj_single_setup_parameters(self, mask, selected_class):
        # for mask in current_masks:
        #     if selected_class in current_masks:
        #         for node in self.default_setup_nodes:
        #             if 'mask_default' + selected_class in node:
        #                 node.parm('file').set(current_masks)
        for node in self.default_setup_nodes:
            if 'mask_default_' + selected_class in node.name():
                node.parm('file').set('testing')
    
    def _obj_create_single_setup(self, current_masks, classes):
        for mask_list in current_masks:
            for mask in mask_list:
                print(mask)
                for selected_class in classes:
                    print(selected_class)
                    if selected_class in mask:
                        print('called')
                        self._rename_nodes(self._create_default_setup(), selected_class)
                        self._obj_single_setup_parameters(mask, selected_class)

        
        
    
    def _obj_create_multiple_setup(self, all_maps_dict,classes):
        pass
    
    def _lop_create_setup(self):
        pass
    
    def _lop_create_mask_setup(self):
        pass
    
    def _lop_create_normal_setup(self):
        pass

    def _lop_create_material_setup(self):
        pass
    
    def _create_default_setup(self):
        nodes_created = self.geometry.copyItems(self.default_setup_nodes)
        self._create_NetworkBox(nodes_created)
        return nodes_created
        
    def _rename_nodes(self, nodes, rename_string):
        for node in nodes:
            node.setName(node.name()[:-1] + '_' + rename_string)
            
        #update references
        for index in range(len(self.default_setup_nodes)):
            self.default_setup_nodes[index] = nodes[index]
            
            
    # def _create_object_structure(self, background_maps, all_maps_dict, current_masks, b_mix_multiple_instances ):
    #     self._obj_set_references()
        
    #     if b_mix_multiple_instances:
    #         self._create_extra_setup()
    #     else: 
    #         self.create
    #     # for class_types in classes:
    #     #     self._rename_nodes(self._create_default_setup(), class_types)
        
    #     self._fix_layout(self.geometry)
        
    # def _lop_create_structure(self):
    #     pass
    
    
    def setup_houdini(self, background_maps, all_maps_dict, current_masks, classes, b_mix_multiple_instances):
        self._obj_set_references()
        self._lop_set_references()

        if b_mix_multiple_instances:
            self._obj_create_multiple_setup(all_maps_dict, classes)
        else:
            self._obj_create_single_setup(current_masks, classes)
            
        self._lop_create_setup()
        
        self._fix_layout(self.geometry)
        self._fix_layout(self.lop)
    
    
                    
    def preprocess_3D_asset_masks(self):
        # loading UV_baking.hip
        try:
            hou.hipFile.load(self.paths.get_uv_hip_file())
        except hou.LoadWarning as e:
            print(e)
        # set resolution for unwrapping, takes around 3min for 1 3d-asset. Could possibly be optimized. Currently renders with CPU only.
        resolution = self.settings.get_UV_baking_resolution()
        resolution_str = str(int(resolution / 1024))
        hou.node("/out/baketexture").parm("vm_uvunwrapresx").set(resolution)
        hou.node("/out/baketexture").parm("vm_uvunwrapresy").set(resolution)
        #  initilize variables for current example
        masked_3d_dir = self.paths.get_masked_3D_folder()
        temp_UV_baking_folder = self.paths.get_uv_temp_folder()
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
