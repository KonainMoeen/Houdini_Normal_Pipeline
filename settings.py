
class Settings():
    def __init__(self):
        pass
    
    # Enter in priority # Higher to Lower
    def get_all_classes(self):
        priority_list = ['green_lichen', 'white_lichen', 'moss', "yellow_lichen"]
        priority_list.reverse()
        return priority_list
    
    def get_all_maps(self):
        return ['albedo', 'normal', 'roughness'] + self.get_all_classes()
    
    def get_UV_baking_resolution(self):
        return 8192
    
    def get_render_file_format(self):
        return 'exr'
    
    def get_render_resolution(self):
        return 2048
    
    def get_delete_small_parts_threshold(self):
        threshold = {}
        threshold['default'] = [0.001,0.001,0]
        threshold['green_lichen'] = [0.001,0.001,0]
        threshold['white_lichen'] = [0.001,0.001,0]
        threshold['moss'] = [0.01,0.01,0]

        return threshold
    
    # def get_scale_multiplier(self):
    #     scale = {}
    #     scale['default'] = 1
    #     scale['green_lichen'] = 1
    #     scale['white_lichen'] = 1
    #     scale['moss'] = 1
    #     return scale
    
    def get_total_count(self): #configure instance count
        # total - random value between 0 to max amount to subtract
        # to add new class : 
        #   no_of_points['class_name'] = 'max number of points - random
        no_of_points = {}
        no_of_points['default'] = '100 - fit(rand($F * 12431),0,1,0,50)' 
        no_of_points['green_lichen'] = '200 - fit(rand($F * 25234),0,1,0,100)'
        no_of_points['white_lichen'] = '30 - fit(rand($F * 1212),0,1,0,20)'
        no_of_points['moss'] = '100 - fit(rand($F * 12431),0,1,0,50)'

        return no_of_points
    
    #sorting mesh positions for more randomization
    def get_point_sort(self):   # 2=x  3=y  4=z  5=reverse  6=random
        sort = {}
        sort['default'] = 0
        sort['green_lichen'] = 0
        sort['white_lichen'] = 0
        sort['moss'] = 0

        return sort
    
    # randomizes scale between the minimum and maximum values
    def get_randomize_scale_values(self):
        scale_max = {}
        scale_min  = {}
        
        scale_min['default'] = 1
        scale_min['green_lichen'] = 1
        scale_min['white_lichen'] = 1
        scale_min['moss'] = 1
        
        scale_max['default'] = 2
        scale_max['green_lichen'] = 2
        scale_max['white_lichen'] = 2
        scale_max['moss'] = 2
            
        scale = [scale_min, scale_max]
        return scale