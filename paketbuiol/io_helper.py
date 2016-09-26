from itertools import islice,chain 
import os, glob, shutil

class BatchReader(object):

    def __init__(self, batch_size, iterator=None, file_path=""):
        
        if file_path != "":
            self.iterator = open(file_path, "r")
        else:
            assert iterator is not None, "Iterator cannot be None"
            self.iterator= iterator

        self.batch_size= batch_size

    def __iter__(self):
        return self.next()

    def next(self):
        yield self.__batch(self.iterator, self.batch_size)
    

    def __batch(self,iterable, size):
        """Gets items in batches from a sequence/iterable
        
        Args:

        * iterable (iterable) : Any collection of FastQ sequences (not the FastQ Sequence object) that implements the next() and __iter__() methods
        * size (int): Number of sequences to be processed in batches

        Returns:
        
        * An iterable object comprising data chunks from the input file

        """

        sourceiter = iter(iterable)
        while True:
            batchiter = islice(sourceiter, size)
            yield chain([batchiter.next()], batchiter)


class OutputDirTailor(object):
    """
        Initiates an output directory for analyses yielding various outputs.
        input_data_structure: 
            {

                root: ".",
                outputdir: root/project_name/outputs
                tables: list_of_output_table_dirs
                figures: list_of_output_figure_dirs
                tmp_dir: "root/project_name/tmp" analysis results of the previous run.

            }
    """
    def __init__(self, project_name, root_path=".", data_categories=[]):
        self.project_name= project_name
        self.root_path= root_path
        self.data_categories= data_categories
        

    def init_project_dir(self):
        self.output_dir= os.path.join(self.root_path, self.project_name, "outputs")
        self.tmp_dir= os.path.join(self.root_path, self.project_name, "tmp")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        if os.path.exists(self.output_dir):
            msg= "There is an existing project in the directory you mentioned.\n\
Do you want to delete the existing project? \n(yes/no, y/n): "
            #response= raw_input(msg)
            #if response == "yes" or response == "y":
            self.rm_previous()
            self.init_output_dir()
    
        else:
            self.init_output_dir()

    def init_output_dir(self):
        
        for category in self.data_categories:
            os.makedirs(os.path.join(self.output_dir, "tables", str(category)))
            os.makedirs(os.path.join(self.output_dir, "figures", str(category)))


    def rm_previous(self):
    
        tmp_tables= os.path.join(self.tmp_dir, "tables")
        tmp_figures= os.path.join(self.tmp_dir, "figures")

        if os.path.exists(tmp_tables):
            shutil.rmtree(tmp_tables)
        if os.path.exists(tmp_figures):
            shutil.rmtree(tmp_figures)

        old_outputs = glob.glob(os.path.join(self.output_dir, "*"))
        
        for output in old_outputs:
            shutil.move(output, self.tmp_dir)
        

    def get_output_table_dir(self, category):
        return os.path.join(self.output_dir, "tables", str(category))

