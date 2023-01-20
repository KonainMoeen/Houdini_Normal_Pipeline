import hou
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
import numpy as np
from PIL import Image
import cv2
from paths import Paths
from settings import Settings
from pprint import pprint
from random import randint

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
        blast = self.geometry.node('blast_default')
        out = self.geometry.node('OUT')
        
        self.default_setup_nodes = [mask, uv, foreach_begin, delete_small_parts, center_position,foreach_end, group, merge,connectivity,scatter,randomize_rotations,sort,attribute_from_pieces,copytopoints, reverse, attribdelete, transform, blast, out]
        self.extra_setup_nodes = [mask, uv, foreach_begin, delete_small_parts, center_position,foreach_end, group]
        
    def _lop_set_references(self):
        self.lop = hou.node('/obj/Render')
        self.sop_import = hou.node('/obj/Render/sop_default')
        # for mask
        mask_render_settings = self.lop.node('karmarendersettings_default_mask')
        mask_render = self.lop.node('render_default_mask')
        #for albedo
        merge = self.lop.node('merge_all_albedo')
        albedo_material_library = self.lop.node('materiallibrary_albedo')
        albedo_render_settings = self.lop.node('karmarendersettings_default_albedo')
        albedo_render = self.lop.node('render_default_albedo')
        # for normal
        normal_material_library = self.lop.node('materiallibrary_default_normal')
        normal_render_settings = self.lop.node('karmarendersettings_default_normal')
        normal_render = self.lop.node('render_default_normal')
        self.lop_mask_nodes = (mask_render, mask_render_settings)
        self.lop_albedo_nodes = (merge, albedo_material_library, albedo_render_settings, albedo_render)
        self.lop_normal_nodes = (normal_material_library, normal_render_settings, normal_render)
            
    def _create_setup(self,context,nodes):
        nodes_created = context.copyItems(nodes)
        self._create_NetworkBox(nodes_created)
        return nodes_created
        
    def _rename_nodes(self, nodes, rename_string):
        for node in nodes:
            node.setName(node.name()[:-1] + '_' + rename_string)
        return nodes
    
    def _obj_setup_default_parameters(self, current_masks_dict, key):
        hou.node('/obj/Geometry/mask_default_' + key).parm('file').set(current_masks_dict[key][0])
        hou.node('/obj/Geometry/delete_small_parts_default_' + key).parmTuple('threshold').set(self.settings.get_delete_small_parts_threshold()[key])
        hou.node('/obj/Geometry/center_position_default_' + key).parm('Scale_Multiplier').set(self.settings.get_scale_multiplier()[key])
        hou.node('/obj/Geometry/group_default_' + key).parm('groupname').set(key)
        hou.node('/obj/Geometry/scatter_default_' + key).parm('npts').setExpression(self.settings.get_total_count()[key])
        hou.node('/obj/Geometry/sort_default_' + key).parm('ptsort').set(self.settings.get_point_sort()[key])
        hou.node('/obj/Geometry/transform_default_' + key).parmTuple('t').set([0,0,(self.settings.get_all_classes().index(key) + 1) * 10])
        hou.node('/obj/Geometry/blast_default_' + key).parm('group').set(key)
        
        self.out_nodes.append(hou.node('/obj/Geometry/OUT_' + key))

    def _obj_setup_extra_parameters(self, selected_map, key, index):
        hou.node('/obj/Geometry/mask_default_' + key + '_' + str(index)).parm('file').set(selected_map)
        hou.node('/obj/Geometry/delete_small_parts_default_' + key + '_' + str(index)).parmTuple('threshold').set(self.settings.get_delete_small_parts_threshold()[key])
        hou.node('/obj/Geometry/center_position_default_' + key + '_' + str(index)).parm('Scale_Multiplier').set(self.settings.get_scale_multiplier()[key])
        hou.node('/obj/Geometry/group_default_' + key + '_' + str(index)).parm('groupname').set(key + '_' + str(index))
    
    def _obj_combine_setups(self, key, index):
        hou.node('/obj/Geometry/merge_default_' + key).setNextInput(hou.node('/obj/Geometry/group_default_' + key + '_' + str(index)))
    
    def _obj_create_out_structure(self, key, index):
        blast_node = hou.node('/obj/Geometry').createNode('blast')
        blast_node.setName('blast_' + key + '_' + str(index))
        blast_node.setInput(0, hou.node('/obj/Geometry/transform_default_' + key))
        blast_node.parm('group').set(key + '_' + str(index))
        blast_node.parm('negate').set(1)
        
        out_node = hou.node('/obj/Geometry').createNode('null')
        out_node.setName('OUT_' + key + '_' + str(index))
        out_node.setInput(0, blast_node)
        
        self.out_nodes.append(out_node)
            
    def _obj_create_setup(self, all_maps_dict, current_masks_dict, classes_list, b_mix_multiple_instances):
        if b_mix_multiple_instances:
            for key in all_maps_dict.keys():
                if key in classes_list and key:
                    self._rename_nodes(self._create_setup(self.geometry,self.default_setup_nodes), key)
                    self._obj_setup_default_parameters(all_maps_dict,key)
                    for index, selected_map in enumerate(all_maps_dict[key][1:]):
                        self._rename_nodes(self._create_setup(self.geometry,self.extra_setup_nodes), key + '_' + str(index))
                        self._obj_setup_extra_parameters(selected_map, key, index)
                        self._obj_combine_setups(key,index)
                        self._obj_create_out_structure(key,index)
        else:
            for key in current_masks_dict.keys(): 
                self._rename_nodes(self._create_setup(self.geometry,self.default_setup_nodes), key)
                self._obj_setup_default_parameters(current_masks_dict,key)
                    
    
    def _lop_create_setup(self, background_maps, all_maps_dict, classes_list, b_mix_multiple_instances):
        if b_mix_multiple_instances:
            for selected_class in classes_list:
                merge_node = self.lop.createNode('merge')
                merge_node.setName('merge_sop_' + selected_class)
                self._rename_nodes(self._create_setup(self.lop, self.lop_mask_nodes), selected_class)
                self._rename_nodes(self._create_setup(self.lop, self.lop_normal_nodes), selected_class)
                for index,node in enumerate(self.out_nodes):
                    if selected_class in node.name():
                        node_name = "_".join(node.name().split('_')[1:])
                        sop_node = self.lop.createNode('sopimport')
                        sop_node.setName('sop_default_' + node_name)
                        sop_node.parm('soppath').set(node.path())
                        sop_node.setInput(0,self.lop.node('camera'))
                        merge_node.setNextInput(sop_node)
                        self._lop_create_materials(all_maps_dict, node_name, index, selected_class)

                hou.node('/obj/Render/merge_all_albedo').setNextInput(merge_node )
                hou.node('/obj/Render/karmarendersettings_default_mask_' + selected_class).setInput(0,merge_node)
                hou.node('/obj/Render/materiallibrary_default_normal_' + selected_class).setInput(0,merge_node)            
        else:
            for index,node in enumerate(self.out_nodes):            
                node_name = "_".join(node.name().split('_')[1:])
                sop_node = self.lop.createNode('sopimport')
                sop_node.setName('sop_default_' + node_name)
                sop_node.parm('soppath').set(node.path())
                sop_node.setInput(0,self.lop.node('camera'))
                self._rename_nodes(self._create_setup(self.lop, self.lop_mask_nodes), node_name)
                self._rename_nodes(self._create_setup(self.lop, self.lop_normal_nodes), node_name)
                self._lop_combine_setup(index, node_name, sop_node)
                self._lop_create_materials(all_maps_dict, node_name, index, node_name)

        self._lop_setup_background_material_maps(background_maps)

    def _lop_create_materials(self, all_maps_dict, node_name, index, selected_class):
        maps_type_list = self.settings.get_all_maps()
        for maps_type in maps_type_list:
            if maps_type not in self.settings.get_all_classes():
                material =hou.copyNodesTo((self.lop.node(maps_type + '_materials/default_' + maps_type),), self.lop.node(maps_type + '_materials'))
                material[0].setName(node_name + '_' + maps_type)
                self._lop_setup_material_maps(all_maps_dict, maps_type, material[0])

                material_library = self.lop.node('materiallibrary_' + maps_type)
                if maps_type == 'normal': # because we want normals separately for our compositing
                    material_library = self.lop.node('materiallibrary_default_normal_' + selected_class)
                    material_library.parm('materials').set(len(self.out_nodes))
                    material_library.parm('geopath'+ str(index + 1)).set('/sop_default_' +  node_name + '/')
                    material_library.parm('matnode'+ str(index + 1)).set('../' + maps_type + '_materials/' + node_name + '_' + maps_type )
                else:
                    # to make space for background geometry and materials
                    material_library.parm('materials').set(len(self.out_nodes) + 1)
                    material_library.parm('geopath'+ str(index + 2)).set('/sop_default_' +  node_name + '/')
                    material_library.parm('matnode'+ str(index + 2)).set('../' + maps_type + '_materials/' + node_name + '_' + maps_type)
                    
                
    def _lop_setup_background_material_maps(self,background_maps):
        for maps_type in self.settings.get_all_maps():
            if maps_type not in self.settings.get_all_classes():
                for maps in background_maps:
                    if maps_type + '.' in maps:
                        self.lop.node(maps_type + '_materials/bg_surface_' + maps_type + '/mtlxUsdUVTexture').parm('file').set(maps)
        
    def _lop_setup_material_maps(self,all_maps_dict, maps_type, material):
        node_name =  '_'.join(material.name().split('_')[:-1])
        mask_file = self.geometry.node('mask_default_' + node_name).parm('file').eval()
        texture_id = mask_file.split('\\')[-1].split('_')[0]
        
        for maps in all_maps_dict[maps_type]:
            if texture_id in maps:
                material.node('mtlxUsdUVTexture').parm('file').set(maps)
    
    def _lop_combine_setup(self, index, node_name, node):
        hou.node('/obj/Render/merge_all_albedo').setNextInput(node )
        hou.node('/obj/Render/karmarendersettings_default_mask_' + node_name).setInput(0,node)
        hou.node('/obj/Render/materiallibrary_default_normal_' + node_name).setInput(0,node)
    
    def setup_houdini(self, background_maps, all_maps_dict, current_masks_dict, classes_list, b_mix_multiple_instances, batch_index, index):
        self.out_nodes = []

        self._obj_set_references()
        self._lop_set_references()

        self._obj_create_setup(all_maps_dict, current_masks_dict, classes_list, b_mix_multiple_instances)
        self._lop_create_setup(background_maps,all_maps_dict, classes_list, b_mix_multiple_instances)
        self._out_create_setup()
        self._set_output_folder(background_maps[1].split('\\')[-1].split('_')[0], batch_index, index)
                
        self._fix_layout(self.geometry)
        self._fix_layout(self.lop)
    
    def _lop_set_render_settings(self, render_number):
        for node in self.lop.children():
            if 'karmarendersettings_' in node.name():
                if node.name() not in ['karmarendersettings_default_mask', 'karmarendersettings_default_normal']:
                    self._set_render_path(node, render_number)
                    self._set_render_resolution(node)
    
    def _set_render_path(self, node, render_number):
        filename = node.name().replace('karmarendersettings_', '').replace('default_', '')
        node.parm('picture').set(self.render_path +  filename + '_' +  str(render_number) + '.' +  self.settings.get_render_file_format() )
    
    def _set_render_resolution(self, node):
        node.parmTuple('resolution').set((self.settings.get_render_resolution(),self.settings.get_render_resolution()))
        
    def _out_create_setup(self):
        for node in self.lop.children():
            if 'render_' in node.name():
                if node.name() not in ['render_default_mask', 'render_default_normal']:
                    out_node = hou.node('out').createNode('fetch')
                    out_node.setName(node.name())
                    out_node.parm('source').set(node.path())
                    hou.node('out/render_all').setNextInput(out_node)
    
    def _set_output_folder(self, background_map_id, batch_number , index):
        self.render_path = self.paths.get_output_folder() + '/' +  'batch' + str(batch_number + 1) + '/' + background_map_id  + '/' +  str(index + 1) + '/'
    
    def render(self, renders_per_surface, classes_list):
        for render_number in range(renders_per_surface):
            self.setFrameNumber(None)
            self._lop_set_render_settings(render_number + 1)
            hou.node('out/render_all').render(verbose=True, output_progress=True)
            self._render_composite(render_number + 1, classes_list)
    
    def _cop_setup_maps(self, render_number, classes_list):
        composite_nodes_list = []
        for index,selected_class in enumerate(classes_list):
            # create file node
            file_node = hou.node('obj/Composite').createNode('file')
            file_node.setName(selected_class)
            file_node.parm('filename1').set(self.render_path + "normal_" + selected_class + '_' +  str(render_number) + '.' +  self.settings.get_render_file_format() )
            file_node.parmTuple('size').set((self.settings.get_render_resolution(),self.settings.get_render_resolution()))
            
            # create composite node
            if index > 0:
                composite_node = hou.node('obj/Composite').createNode('over')   # 0=over 1=under 6=add
                composite_node.setName('composite_' + str(index))
                composite_nodes_list.append(composite_node)
            elif index == 0:
                hou.node('obj/Composite/background').parm('filename1').set(self.render_path + 'normal_background_' +  str(render_number) + '.' +  self.settings.get_render_file_format() )

        if composite_nodes_list:
            # connect file nodes to composite nodes
            count = 0
            for selected_class in self.settings.get_all_classes():
                if selected_class in classes_list:
                    if count == 0:
                        composite_nodes_list[0].setInput(0, hou.node('obj/Composite/' + selected_class))
                    elif count == 1:
                        composite_nodes_list[0].setInput(1, hou.node('obj/Composite/' + selected_class))
                    else:
                        composite_nodes_list[count-1].setInput(1, hou.node('obj/Composite/' + selected_class))
                    count = count + 1

            # connect composite nodes to composite nodes and connect to vopcop
            for index, composite_node in enumerate(composite_nodes_list):
                if index > 0:
                    composite_node.setInput(0, composite_nodes_list[index - 1])
            hou.node('obj/Composite/vopcop2filter2').setInput(0, composite_nodes_list[-1])
        else:
            hou.node('obj/Composite/vopcop2filter2').setInput(0, hou.node('obj/Composite/' + classes_list[0]))

    def _render_composite(self, render_number, classes_list):
        self._cop_setup_maps(render_number, classes_list)
        self._fix_layout(hou.node('obj/Composite'))
        hou.node('obj/Composite/normal_out').parm('copoutput').set(self.render_path + 'Normal' + '.' + self.settings.get_render_file_format())
        hou.node('obj/Composite/normal_out').render(verbose=True, output_progress=True)
    
    def setFrameNumber(self,frame):
        if frame:
            hou.setFrame(frame)
        else:
            hou.setFrame(randint(0,240))
                    
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
