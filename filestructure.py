from pprint import pprint
from paths import get_assets_path
import os
import itertools


class FileStructureSetup():
    def __init__(self, _asset_type_3d, _asset_type_surface, _asset_type_atlas):

        self.path = get_assets_path()

        self._asset_type_3d = _asset_type_3d
        self._asset_type_surface = _asset_type_surface
        self._asset_type_atlas = _asset_type_atlas

        self._assetfiles_atlas_list, self._assetfiles_3d_list, self._assetfiles_surfaces_list, self._assetfiles_bg_list = [], [], [], []

    # according to the json input check which folders to read

    def _setup_folders_to_search(self):
        folders_to_search = ['\surface']  # for backgorund surfaces
        if self._asset_type_3d:
            folders_to_search.append('masked_3d')
        if self._asset_type_surface:
            folders_to_search.append('masked_surfaces')
        if self._asset_type_atlas:
            folders_to_search.append('atlas_decal')

        return folders_to_search

    # reads all maps and saves them in a dictionary

    def _set_masks(self):

        classes = ["green_lichen", "white_lichen", "moss"]
        self.assetmaps = {'albedo': [], 'normal': [], 'green_lichen': [], 'white_lichen': [], 'moss': []}

        # remove masks according to the json input
        for selected_class in classes:
            if selected_class not in self._asset_type_atlas:
                for index, file_list in enumerate(self._assetfiles_atlas_list):
                    for file in file_list:
                        if selected_class in file.split('\\')[-1] or ('opacity' in file.split('\\')[-1] and selected_class == 'moss'): # not removing the opacity mask in atlas
                            self._assetfiles_atlas_list[index].remove(file)
            if selected_class not in self._asset_type_3d:
                for index, file_list in enumerate(self._assetfiles_3d_list):
                    for file in file_list:
                        if selected_class in file.split('\\')[-1]:
                            self._assetfiles_3d_list[index].remove(file)
            if selected_class not in self._asset_type_surface:
                for index, file_list in enumerate(self._assetfiles_surfaces_list):
                    for file in file_list:
                        if selected_class in file.split('\\')[-1]:
                            self._assetfiles_surfaces_list[index].remove(file)

        filtered_list = self._assetfiles_atlas_list + self._assetfiles_3d_list + self._assetfiles_surfaces_list
                
        # remove folders that have no masks in them
        _ = []
        for lists in filtered_list:
            for items in lists:
                if 'surfacemask' in items or 'opacity' in items:
                    _.append(lists)
                    break
                
        filtered_list = _

        # read all the maps and add them to their key value pairs
        for map_types in filtered_list:
            for map in map_types:
                if '_albedo' in map.split('\\')[-1]:
                    self.assetmaps["albedo"].append(map)
                elif '_normal' in map.split('\\')[-1]:
                    self.assetmaps["normal"].append(map)
                elif '_green_lichen' in map.split('\\')[-1]:
                    self.assetmaps["green_lichen"].append(map)
                elif '_white_lichen' in map.split('\\')[-1]:
                    self.assetmaps["white_lichen"].append(map)
                # because we are using opacity map in atlases instead of masks
                elif '_moss' in map.split('\\')[-1] or 'opacity' in map.split('\\')[-1]:
                    self.assetmaps["moss"].append(map)
                            
        # convert dictionary into a list of lists for itertools -  where each list contains a specific class
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
                        # adding the root path to the files
                        for index, file  in enumerate(files):
                            files[index] = file.replace(file, root.lower() + '/' + file.lower()).replace('/', '\\')
                            
                        # placing files in specific variables according to their folder
                        if folder == 'atlas_decal':
                            self._assetfiles_atlas_list.append(files)
                        elif folder == 'masked_3d':
                            self._assetfiles_3d_list.append(files)
                        elif folder == 'masked_surfaces':
                            self._assetfiles_surfaces_list.append(files)
                        elif folder == '\\surface':
                            self._assetfiles_bg_list.append(files)
                            
        self._set_masks()
                            
    # sends unique lists of maps from classes
    def get_masks_list(self):
        return list(itertools.product(*self.uniqueset))
    
    # sends all of the maps for the current batch in a form of dictionary
    def get_all_maps_dict(self):
        return self.assetmaps
    
    def get_background_maps_list(self):
        return self._assetfiles_bg_list
