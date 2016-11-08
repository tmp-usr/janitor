from storm.locals import Store, create_database


class UniversalDBBase(object):
    def __init__(self, sql_db_path, *args, **kwargs):
        self.sql_db_path= sql_db_path
        self.__init_database()
        self.create_table_strings= {} 
       
        self.generate_create_table_strings()
    
        table_names= map(unicode, self.create_table_strings.keys())
            
        table_list= list(set([table[0] for table in self.store.execute('select tbl_name from SQLITE_MASTER')]))
        
        if table_list == []:
            self.create_tables()
        
        elif sorted(table_list) != sorted(table_names):
            print "db list", sorted(table_list)
            print "expected", sorted(table_names)
            raise Exception("Check tables. Something's wrong")

    @property
    def fullname(self):
        return self.__module__ + "." + self.__class__.__name__
    
    def __init_database(self):    
        """
        creates the sqlite database instance and checks if the database exists in biodb.
        """
        database= create_database("sqlite:%s" % self.sql_db_path)

        print "Created storm database from %s for %s" % (self.sql_db_path, self.fullname)
        self.store= Store(database)
   

    def generate_create_table_strings(self):
        not_implemented_message= """
        example_use: 
                
        self.create_table_strings[table_name]=  self.generate_create_table_string(table_name, 
                                    OrderedDict([(col1, col1_type+" PRIMARY KEY"), (col2, col2_type)]),
                                    OrderedDict([col2:(reference_table, reference_col))) 


        """
        raise NotImplementedError(not_implemented_message)

    
    def create_table(self, table_name):
        self.store.execute(self.create_table_strings[table_name])
        self.store.commit()


    def drop_table(self, table_name):
        drop_table_string= "drop table %s" %table_name 
        self.store.execute(drop_table_string)


    def drop_tables(self, tables):
        
        drop_table_string= "drop table " 
        
        for table in tables:
            drop_table_str= drop_table_string + table
            try:
                self.store.execute(drop_table_str)
            except:
                continue

        self.store.commit()

   
    def create_tables(self):
        for table_name, create_table_string in self.create_table_strings.iteritems():
            print create_table_string
            self.store.execute(create_table_string)
            self.store.commit() 



    def generate_create_table_string(self, table_name, columns, foreign_keys= {}):
        """
            table_name: str
            tables: OrderedDict with fieldname as keys and type as value
            foreign keys: with source_id as keys, and  (target_table, target_id)
            as values
        """
        
        starter= "CREATE TABLE %s " %table_name

        table_str= ""
        for col, col_type in columns.iteritems():
            table_str+= "%s %s, " %(col, col_type)

            
        table_str = "(%s" %table_str.rstrip(', ')
        
        foreign_key_str=""
        for source_id, (target_name, target_id) in foreign_keys.iteritems():
            foreign_key_str+=", FOREIGN KEY (%s) REFERENCES %s (%s)" %(source_id, target_name, target_id)
        
        foreign_key_str+= ");"

        return "".join([starter, table_str, foreign_key_str]) 



