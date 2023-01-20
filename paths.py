import sys

class Paths():
    
    PIPELINE_PATH = "C:/Users/Konain/Documents/HoudiniProjects/Houdini_Normal_Pipeline/"
    
    def __init__(self):
        pass
    
    def get_json_file(self):
        return "configuration.json"
    
    def append_anaconda3_library(self):
        sys.path.append("c:/users/Konain/anaconda3/lib/site-packages")
        
    def get_houdini_path(self):
        return "E:/Houdini/Houdini 19.5.368/"
    
    def get_asset_path(self):
        return self.PIPELINE_PATH + 'assets'
    
    def get_pipeline_hip_file(self):
        return self.PIPELINE_PATH + 'pipeline/HoudiniNormalPipeline.hip'
    
    def get_background_surfaces_folder(self):
        return self.PIPELINE_PATH + 'assets/surface/rock'
    
    def get_masked_3D_folder(self):
        return self.PIPELINE_PATH + 'assets/masked_3d'
    
    def get_masked_surfaces_folder(self):
        return self.PIPELINE_PATH + 'assets/masked_surfaces'
    
    def get_atlas_decal_folder(self):
        return self.PIPELINE_PATH + 'assets/atlas_decal'
    
    def get_output_folder(self):
        return self.PIPELINE_PATH + 'renders/test'
    
    def get_uv_hip_file(self):
        return self.PIPELINE_PATH + 'UV_baking/UV_baking.hip'
    
    def get_uv_temp_folder(self):
        return self.PIPELINE_PATH + 'UV_baking/temp'
