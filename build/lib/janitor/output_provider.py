import os
import shutil

class Output(object):
    def __init__(self, name, path):
        self.name = name
        self.path= path

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path

    @property
    def exists(self):
        return os.path.exists(self.path)


class OutputDir(Output):
    def __init__(self, name, path):
        Output.__init__(self, name, path)

    def init(self, remove_existing= False, create=True):
        if self.exists:
            if remove_existing:
                shutil.rmtree(self.path) 

        if create:
            os.makedirs(self.path)


class OutputFile(Output):
    def __init__(self, name, path):
        Output.__init__(self, name, path)



class OutputProvider(object):
    """
        root (project_name_outputs)
            - 

    """
    def __init__(self, root_dir, dirs={}, files={}):
        self.root_dir= root_dir
        self.dir_paths= dirs
        self.file_paths= files

        self.output_dirs= []
        self.output_files= []

        self._init_outputs()

    def get_dir(self, name):
        return [out_dir for out_dir in self.output_dirs if out_dir.name == name][0]

    def get_file(self, name):
        return [out_file for out_file in self.output_files if out_file.name == name][0]

    def _init_outputs(self):
        self.__init_root()
        self.__init_dirs()
        self.__init_files()

    def __init_root(self):
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

    def __init_dirs(self):
        for name, path in self.dir_paths.iteritems():
           
            o_dir= OutputDir(name, path)
            
            if "tmp" in name:
                o_dir.init(remove_existing= True, create= False)        
            
            elif "ref" in name:
                o_dir.init(remove_existing= False, create= False)
            
            else:    
                o_dir.init(remove_existing= True, create=True)
            
            self.__dict__.update({name: o_dir}) 

    def __init_files(self):
        for name, path in self.file_paths.iteritems():
            o_file= OutputFile(name.replace("_file",""), path)
            self.__dict__.update({name: o_file})  
    
