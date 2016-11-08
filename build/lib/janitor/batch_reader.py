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



