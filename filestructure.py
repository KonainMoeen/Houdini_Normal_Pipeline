# import json
# from paths import get_json_file
from pprint import pprint
from paths import get_assets_path
import os
import itertools


class FileStructureSetup():
    def __init__(self, asset_type_3d, asset_type_surface, asset_type_atlas):

        self.path = get_assets_path()

        self.asset_type_3d = asset_type_3d
        self.asset_type_surface = asset_type_surface
        self.asset_type_atlas = asset_type_atlas

        self.assetfiles_atlas, self.assetfiles_3d, self.assetfiles_surfaces, self.assetfiles_bg = [], [], [], []

    # according to the json input check which folders to read

    def _setup_folders_to_search(self):
        folders_to_search = ['\surface']  # for backgorund surfaces
        if self.asset_type_3d:
            folders_to_search.append('masked_3d')
        if self.asset_type_surface:
            folders_to_search.append('masked_surfaces')
        if self.asset_type_atlas:
            folders_to_search.append('atlas_decal')

        return folders_to_search

    # reads all maps and saves them in a dictionary

    def _set_masks(self):

        classes = ["green_lichen", "white_lichen", "moss"]
        self.assetmaps = {'albedo': [], 'normal': [], 'green_lichen': [], 'white_lichen': [], 'moss': []}

        # remove masks according to the json input
        for sel_class in classes:
            if sel_class not in self.asset_type_atlas:
                for index, file_list in enumerate(self.assetfiles_atlas):
                    for file in file_list:
                        if sel_class in file or ('opacity' in file.lower() and sel_class == 'moss'): # not removing the opacity mask in atlas
                            self.assetfiles_atlas[index].remove(file)
            if sel_class not in self.asset_type_3d:
                for index, file_list in enumerate(self.assetfiles_3d):
                    for file in file_list:
                        if sel_class in file:
                            self.assetfiles_3d[index].remove(file)
            if sel_class not in self.asset_type_surface:
                for index, file_list in enumerate(self.assetfiles_surfaces):
                    for file in file_list:
                        if sel_class in file:
                            self.assetfiles_surfaces[index].remove(file)

        filtered_list = self.assetfiles_atlas + self.assetfiles_3d + self.assetfiles_surfaces

        # remove folders that have no masks in them
        _ = []
        for lists in filtered_list:
            for items in lists:
                if 'surfacemask' in items.lower() or 'opacity' in items.lower():
                    _.append(lists)
                    break
                
        filtered_list = _

        # read all the classes and add them to their key value pairs
        for listofassettypes in filtered_list:
            for map in listofassettypes:
                if '_albedo' in map.lower():
                    self.assetmaps["albedo"].append(map)
                elif '_normal' in map.lower():
                    self.assetmaps["normal"].append(map)
                elif '_green_lichen' in map.lower():
                    self.assetmaps["green_lichen"].append(map)
                elif '_white_lichen' in map.lower():
                    self.assetmaps["white_lichen"].append(map)
                # because we are using opacity map in atlases instead of masks
                elif '_moss' in map.lower() or 'opacity' in map.lower():
                    self.assetmaps["moss"].append(map)
        
        # converting dictionary into a list of lists for itertools -  where each list contains a specific class
        self.uniqueset = []
        if len(self.assetmaps['green_lichen']) > 0:
            self.uniqueset.append(self.assetmaps['green_lichen'])
        if len(self.assetmaps['white_lichen']) > 0:
            self.uniqueset.append(self.assetmaps['white_lichen'])
        if len(self.assetmaps['moss']) > 0:
            self.uniqueset.append(self.assetmaps['moss'])
            
    # read all the folder and files in the assets folder and save the files in variables
    def read_files(self):
        for root, dir, files in os.walk(self.path):
            for folder in self._setup_folders_to_search():
                if folder in root:
                    if files:
                        if folder == 'atlas_decal':
                            self.assetfiles_atlas.append(files)
                        elif folder == 'masked_3d':
                            self.assetfiles_3d.append(files)
                        elif folder == 'masked_surfaces':
                            self.assetfiles_surfaces.append(files)
                        elif folder == '\\surface':
                            self.assetfiles_bg.append(files)
                            
        self._set_masks()

    def get_maps_set(self):
        return list(itertools.product(*self.uniqueset))
    
    def get_maps_per_class(self):
        # _ = list()
        # _.append(self.assetfiles_atlas)
        # _.append(self.assetfiles_3d)
        # _.append(self.assetfiles_surfaces)
        
        return self.assetmaps
