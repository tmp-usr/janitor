import getopt, sys
from itertools import islice,chain 


starter='FastQPolish 1.4 Copyright (C) Sanli et al. (2012) \nReleased under the GNU-GPL version 3 software license.'
license= 'FastQPolish 1.4 Copyright (C) Sanli et al. (2012)\nReleased under the GNU-GPL version 3 software license. This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.'




class Sequence():
    """FastQ Sequence object."""
    def __init__(self,seqID='',sequence='',spacer='+',quality=''):
        """Constructor method of the Fastq Sequence object. 
        
        Kwargs:

        * seqID (str): First line of a Fastq Sequence object representing the unique identifier
        * sequence (str): Second line of a Fastq Sequence object representing the DNA sequence
        * spacer (str): Third line of a Fastq Sequence object representing the spacer; by default a plus '+' sign. 
        * quality (str): Fourth line of a Fastq Sequence object representing the Phred quality scores
        
        """
        self.id=seqID # identifier
        self.sequence=sequence # sequence 
        self.spacer=spacer # spacer 
        self.quality=quality # quality 


    def get_sequence(self):
        """FastQ Sequence getter method 
        
        Returns:

        * FastQ Sequence (str): Four attributes (lines) of a FastQ sequence object are concatenated and returned 
            
        """
        return self.id+'\n'+self.sequence+'\n'+self.spacer+'\n'+self.quality+'\n'


    def set_sequence(self,ID,sequence,quality,spacer='+'):         
        """Sequence setter method """    
        self.id=ID 
        self.sequence=sequence
        self.quality=quality
        self.spacer=spacer 

    def __str__(self):
        """ __str__ method overriding
        
        Returns:

        * fastq sequence (str): four lines of the fastq sequence concatenated  

        """
        return self.id+'\n'+self.sequence+'\n'+self.spacer+'\n'+self.quality+'\n'




class FastQParser():
    """FastQParser object"""
    def __init__(self,handle):
        """constructor method of the Fastq Parser object. 
        
        Args:

        * handle (iterable): any iterable including fastq sequences: e.g an open fastq file object.
        
        """

        self.handle=handle
    
    
    @property
    def fastq_sequences(self):
        """ Fastq Parser setter method. A generator method for Fastq Sequence iterators.
               
        """
        while True:  
            seqID=self.handle.next().rstrip()
            sequence=self.handle.next().rstrip()
            spacer=self.handle.next().rstrip()
            quality=self.handle.next().rstrip()
            yield Sequence(seqID,sequence=sequence,quality=quality,spacer=spacer) 



    
