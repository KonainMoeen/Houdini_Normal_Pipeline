import hou

class HoudiniSetup():
    def __init__(self, path):
        self.path = path
    
    # loads hip file for our script
    def load_hipfile(self, filename):
        try:
            hou.hipFile.load(filename)
        except hou.LoadWarning as e:
            print(e)
            
            
    # sets the path of input files in normal composite hip file
    def _setup_composite_input_files(self):
        hou.node('obj/cop2net1/moss').parm('filename1').set(self.path + 'Moss_Normal.exr')
        hou.node('obj/cop2net1/white_lichen').parm('filename1').set(self.path + 'White_Lichen_Normal.exr')
        hou.node('obj/cop2net1/green_lichen').parm('filename1').set(self.path + 'Green_Lichen_Normal.exr')

    # sets the path of input files in main hip file
    def set_input_files(self, background, index, files_list):
        for file in files_list[index]:
            if "albedo" in file:
                self.current_albedo = file  
                # hou.node('obj/main/Green_Lichen/albedo').set(file)
                # hou.node('obj/main/White_Lichen/albedo').set(file)
                # hou.node('obj/main/Moss/albedo').set(file)
            elif "green_lichen" in file:
                self.current_green_lichen = file  
                 #hou.node('obj/main/Green_Lichen/file').set(file)
            elif "white_lichen" in file:
                self.current_white_lichen = file  
                 #hou.node('obj/main/White_Lichen/file').set(file)
            elif "moss" in file:
                self.current_moss = file  
                 #hou.node('obj/main/Moss/file').set(file)
    
    def set_materials(background):
        pass
    
    # sets the path of main renders 
    def _set_render_path(self):
        hou.parm('/obj/lopnet1/karmarendersettings2/picture').set(self.path + 'Green_Lichen_Mask.exr')
        hou.parm('/obj/lopnet1/karmarendersettings3/picture').set(self.path + 'White_Lichen_Mask.exr')
        hou.parm('/obj/lopnet1/karmarendersettings4/picture').set(self.path + 'Moss_Mask.exr')
        hou.parm('/obj/lopnet1/karmarendersettings/picture').set(self.path + 'Albedo.exr')
        hou.parm('/obj/lopnet1/karmarendersettings1/picture').set(self.path + 'BG_Normal.exr')
        hou.parm('/obj/lopnet1/karmarendersettings5/picture').set(self.path + 'Green_Lichen_Normal.exr')
        hou.parm('/obj/lopnet1/karmarendersettings6/picture').set(self.path + 'White_Lichen_Normal.exr')
        hou.parm('/obj/lopnet1/karmarendersettings7/picture').set(self.path + 'Moss_Normal.exr')

    
    #renders the image from lops-karma
    def render(self):
        self._set_render_path()
        hou.node('/out/render_all').render(verbose=True, output_progress=True)
        
    # sets the normal composite output file location 
    def _set_composite_render_path(self):
        hou.parm('obj/cop2net1/normal_out/copoutput').set(self.path + "Normal.exr")
    
    #renders the composited image
    def render_composite(self):
        self._setup_composite_input_files()
        self._set_composite_render_path()
        hou.node('/obj/cop2net1/normal_out').render(verbose=True, output_progress=True)
        
    # save the hip file with increment
    def save_and_increment_file():
        hou.hipFile.saveAndIncrementFileName()