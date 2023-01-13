import json
from New_paths import Paths
from filestructure import FileStructureSetup
from pprint import pprint

class Main():
    def __init__(self):
        self.paths = Paths()
        self.paths.append_anaconda3_library()
    
    def read_configuration(self):
        jsonObj = json.load(open(self.paths.get_json_file()))
        return jsonObj['batches']
    
    def get_classes(self, batch_index, batches):
        classes = list()
        for class_type in batches[batch_index]['asset_types'].values():
            classes += class_type
        return list(set(classes))
    
    def execute_pipeline(self):
        from New_houdini_setup import HoudiniSetup
        
        batches = self.read_configuration()
        
        for batch_index in range(len(batches)):
            
            classes = self.get_classes(batch_index,batches)
                        
            renders_per_surface = batches[batch_index]['min_num_samples']
            if renders_per_surface == 0: continue

            asset_types_3d = batches[batch_index]['asset_types']['3D']
            asset_types_surface = batches[batch_index]['asset_types']['surface']
            asset_types_atlas = batches[batch_index]['asset_types']['atlas']
            intensity_multiplier = batches[batch_index]['scatter_percent']
            b_mix_multiple_instances = batches[batch_index]['mix_multiple_instances']
            
            houObj = HoudiniSetup()
            # if any(asset_types_3d):
            #     print("Preprocessing UV islands for 3D Assets")
            #     houObj.preprocess_3D_asset_masks()
            #     print("Done Creating masks for UV islands all 3D Assets")
                
            # Using the json input, read the asset maps and setup the render structure
            fileObj = FileStructureSetup(asset_types_3d, asset_types_surface, asset_types_atlas, classes)
            fileObj.read_files()
            
            if not b_mix_multiple_instances:
                # each unique iteration will create a unique folder
                total_unique_iterations = (len(fileObj.get_all_maps_dict()['green_lichen']) if len(fileObj.get_all_maps_dict()['green_lichen']) > 0  else 1 ) * (len(fileObj.get_all_maps_dict()['white_lichen']) if len(fileObj.get_all_maps_dict()['white_lichen']) > 0  else 1 ) * (len(fileObj.get_all_maps_dict()['moss']) if len(fileObj.get_all_maps_dict()['moss']) > 0  else 1 )
            else:
                total_unique_iterations = 1
            
            #pprint(fileObj.get_all_maps_dict())
            #pprint(fileObj.get_unique_mask_structure(classes))
            #pprint(fileObj.get_background_maps_list())
            
            for background_maps in fileObj.get_background_maps_list():
                for index in range(total_unique_iterations):
            
            
                    houObj.load_hipfile(self.paths.get_pipeline_hip_file())
                    houObj.setup_houdini( background_maps, fileObj.get_all_maps_dict(), fileObj.get_unique_mask_structure(classes), classes, b_mix_multiple_instances)
                    houObj.save_and_increment_hip_file()
            
            

    
    
    
    
if __name__ == '__main__':
    Main().execute_pipeline()