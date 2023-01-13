
class Settings():
    def __init__(self):
        pass
    
    def get_all_classes(self):
        return ['green_lichen', 'white_lichen', 'moss']
    
    def get_all_maps(self):
        return ['albedo', 'normal', 'white_lichen', 'moss', 'green_lichen']
    
    def get_UV_baking_resolution(self):
        return 8192
    
    def get_render_file_format(self):
        return 'exr'
    
    def get_render_resolution(self):
        return 2048