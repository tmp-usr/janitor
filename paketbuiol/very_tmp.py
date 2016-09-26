from paketbuiol.io_helper import BatchReader
a= range(100)
handle= BatchReader(10, a)

for chunk in handle:
    #print len(list(chunk))
    for chain in chunk:
        
        #print len(list(item))
        for item in chain:
            #print len(list(chain))
        #    for n in chain:
            print item
