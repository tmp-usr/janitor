import os
import shutil





class IO(object):
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


class IODir(IO):
    def __init__(self, name, path):
        IO.__init__(self, name, path)

    def init(self, remove_existing= False, create=True):
        if self.exists:
            if remove_existing:
                shutil.rmtree(self.path) 
            
        if create:
            os.makedirs(self.path)


class IOFile(IO):
    def __init__(self, name, path):
        IO.__init__(self, name, path)


class IOProvider(object):
    def __init__(self, root_dir, dirs={}, files={}):
        self.root_dir= root_dir
        self.dir_paths= dirs
        self.file_paths= files

        self._init_io()

    def get_dir(self, name):
        return [out_dir for out_dir in self.output_dirs if out_dir.name == name][0]

    def get_file(self, name):
        return [out_file for out_file in self.output_files if out_file.name == name][0]

    def _init_io(self):
        self.__init_root()
        self._init_dirs()
        self._init_files()

    def __init_root(self):
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        
    def _init_dirs(self):
        """
            To be overrriden.
        """
        pass
    
    def _init_files(self):
        """
            To be overriden.
        """
        

class InputProvider(IOProvider):
    def __init__(self, root_dir, dirs= {}, files= {}):
        IOProvider.__init__(self, root_dir, dirs, files)

    def _init_dirs(self):
        for name, path in self.dir_paths.iteritems():
            i_dir= IODir(name, path)
            i_dir.init(remove_existing = False, create= False)
            self.__dict__.update({name: i_dir})

    def _init_files(self):
        for name, path in self.file_paths.iteritems():
            i_file= IOFile(name, path)
            self.__dict__.update({name: i_file})


class OutputProvider(IOProvider):
    def __init__(self, root_dir, dirs= {}, files= {}):
        IOProvider.__init__(self, root_dir, dirs, files)
        
    def _init_dirs(self):
        for name, path in self.dir_paths.iteritems():
            o_dir= IODir(name, path)
            o_dir.init(remove_existing = True, create= True)
            self.__dict__.update({name: o_dir})

    def _init_files(self):
        for name, path in self.file_paths.iteritems():
            i_file= IOFile(name, path)
            self.__dict__.update({name: i_file})


class TmpProvider(IOProvider):
    
    def __init__(self, root_dir, dirs= {}, files= {}, create= False):
        self.create= create 
        IOProvider.__init__(self, root_dir, dirs, files)
        
    def _init_dirs(self):
        for name, path in self.dir_paths.iteritems():
            t_dir= IODir(name, path)
            t_dir.init(remove_existing = True, create= self.create)
            self.__dict__.update({name: t_dir})

    def _init_files(self):
        for name, path in self.file_paths.iteritems():
            t_file= IOFile(name, path)
            self.__dict__.update({name: t_file})





trash= """
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
""" 
