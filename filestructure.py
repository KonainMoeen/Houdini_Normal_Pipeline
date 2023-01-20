from pprint import pprint
from paths import Paths
import os
import itertools
from settings import Settings

class FileStructureSetup():
    def __init__(self, _asset_type_3d, _asset_type_surface, _asset_type_atlas, classes_list):
        self._asset_type_3d = _asset_type_3d
        self._asset_type_surface = _asset_type_surface
        self._asset_type_atlas = _asset_type_atlas
        self.classes_list = classes_list
        self._assetfiles_atlas_list, self._assetfiles_3d_list, self._assetfiles_surfaces_list, self._assetfiles_bg_list = [], [], [], []
        
        self.all_maps = Settings().get_all_maps()
        self.all_classes = Settings().get_all_classes()
        self.assetmaps = {}

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

    def _set_masks(self):
        unfiltered_atlas_dict = self._populate_dict(self._assetfiles_atlas_list)
        unfiltered_3d_dict = self._populate_dict(self._assetfiles_3d_list)
        unfiltered_surface_dict = self._populate_dict(self._assetfiles_surfaces_list)

        filtered_atlas_dict = self._filter_dict(self._asset_type_atlas, unfiltered_atlas_dict)
        filtered_3d_dict = self._filter_dict(self._asset_type_3d, unfiltered_3d_dict)
        filtered_surface_dict = self._filter_dict(self._asset_type_surface, unfiltered_surface_dict)
        
        for key in filtered_3d_dict:
            self.assetmaps[key] = filtered_atlas_dict[key] + filtered_3d_dict[key] + filtered_surface_dict[key]

        self.get_unique_mask_structure(self.classes_list)

    def _filter_dict(self, asset_type, unfiltered_dict):
        for key in self.all_classes:
            if key not in asset_type:
                unfiltered_dict[key] = []
        
        return unfiltered_dict
    
    def _populate_dict(self, assetfiles_list):
        maps_dict= dict().fromkeys(self.all_maps, list())
        
        for asset_files in assetfiles_list:
            for file in asset_files:
                for key in maps_dict.keys():
                    if key + '.' in file:
                        maps_dict[key] =  maps_dict[key] + [file]
                        
        return maps_dict
         
    # read all the folder and files in the assets folder and save the files in variables
    def read_files(self):
        for root, dir, files in os.walk(Paths().get_asset_path()):
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
        
    # create unique structure for iterations
    def get_unique_mask_structure(self, classes_list):
        unique_list= []
        for selected_class in classes_list:
            unique_list.append(self.assetmaps[selected_class])
            
        return self._list_to_dict(list(itertools.product(*unique_list)),classes_list)
    
    def _list_to_dict(self, old_list, classes_list):
        list_of_dict = list()
       
        for map_list in old_list:
            temp_dict = dict()
            for index,map in enumerate(map_list):
                temp_dict[classes_list[index]] = [map]
        
                list_of_dict.append(temp_dict)

        return list_of_dict
 
    # sends all of the maps for the current batch in a form of dictionary
    def get_all_maps_dict(self):
        return self.assetmaps
    
    def get_background_maps_list(self):
        return self._assetfiles_bg_list
