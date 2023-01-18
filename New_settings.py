
class Settings():
    def __init__(self):
        pass
    
    
    def get_all_classes(self):
        return ['green_lichen', 'white_lichen', 'moss']
    
    def get_all_maps(self):
        return ['albedo', 'normal'] + self.get_all_classes()
    
    def get_UV_baking_resolution(self):
        return 8192
    
    def get_render_file_format(self):
        return 'exr'
    
    def get_render_resolution(self):
        return 2048
    
    def get_priority(self):
        priority = {}
        priority['green_lichen'] = 1
        priority['white_lichen'] = 2
        priority['moss'] = 3
        return priority
    
    def get_delete_small_parts_threshold(self):
        threshold = {'default' : [0.01,0.01,0]}
        threshold['green_lichen'] = [0.001,0.001,0]
        threshold['white_lichen'] = [0.001,0.001,0]
        threshold['moss'] = [0.01,0.01,0]
        return threshold
    
    def get_scale_multiplier(self):
        scale = {'default' : 1}
        scale['green_lichen'] = 1
        scale['white_lichen'] = 1
        scale['moss'] = 1
        return scale
    
    def get_total_count(self):
        no_of_points = {'default' : '30 - fit(rand($F * 12451),0,1,0,20)'}
        no_of_points['green_lichen'] = '200 - fit(rand($F * 25234),0,1,0,100)'
        no_of_points['white_lichen'] = '30 - fit(rand($F * 1212),0,1,0,20)'
        no_of_points['moss'] = '100 - fit(rand($F * 12431),0,1,0,50)'
        return no_of_points
    
    def get_point_sort(self):   # 2=x  3=y  4=z  5=reverse  6=random
        sort = {'default' : 0}
        sort['green_lichen'] = 0
        sort['white_lichen'] = 0
        sort['moss'] = 0
        return sort