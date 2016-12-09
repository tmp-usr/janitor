class Output(object):
    def __init__(self, name, path):
        self.name = name
        self.path= path

    @property
    def exists(self):
        return os.exists(self.path)


class OutputDir(Output):
    def __init__(self, name, path):
        Output.__init__(self, name, path)

    def create(self, remove_existing= True):
        if self.exists:
            if remove_existing:
                shutil.rmtree(tmp_dir) 
        os.makedirs(self.path)


class OutputFile(Output):
    def __init__(self, name, path):
        Output.__init__(self, name, path)



class ProjectOutput(object):
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


    def _init_outputs(self):
        self.__init_root()
        self.__init_dirs()
        self.__init_files()

    def __init_root(self):
        if not os.exists(self.root_dir):
            os.makedirs(self.root_dir)

    def __init_dirs(self):
        for name, path in self.directories.iteritems():
            if "tmp" in name:
                o_dir= OutputDir(name, path)

            else:
                o_dir= OutputDir(name, path)
                o_dir.create()

            self.output_dirs.append(o_dir)

    def __init_files(self):
        for name, path in self.files.iteritems():
            o_file= OutputFile(name, path)
            self.output_files.append(o_file)    
    
