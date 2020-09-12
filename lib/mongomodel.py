# TODO :- class jsonSchemaModel() : -Implementations pending .refer to test.mongomodel.py file for info

import pymongo

class Errors:

    class SchemaError(Exception):
        pass

    class DuplicateKeyErr(Exception):
        pass

class PrimaryKey:
    pass

class Optional:
    pass

class Date:
    # TODO 
    """ need to create a custome date datatype """
    pass

##################################
# model library wrapping pymongo #
##################################

class DocumentModel(dict):
    """ Verifyes and saves the schema model.This class needs to be inherited and the schema should be a list.
        It gives a doccument styte verification
        *******************
    Usesage/Example:- 
        exampleschema(Model):
            __schema__ = {
                "firstname" : [str,PrimaryKkey]  # Field parameter should be a list
                "middlename"  : [str,Optinal]
                "lastname" : [str]
                "age"  : [int]
            }
        exampleschema.connect()     # connect to collection 
        doc = excampleschema({"documents":"detalis"})
        doc.dbname.collectionname.insert() or doc.dbname.collectionname.findone()

        *******************
    ##################
    Implemented methods:
    ##################
    ~params:: insert(self,*addtodoc) 
        :- usesage::- doc.db.collection.insert() or doc.db.collection.insert({"appened":"info to the main doc and save"})
    
    ~params:: connect(cls,dburi="mongodb://localhost:27017/",username=None,password=None))
        :- usesage .classmethod to connect to the db .Should be called before any oporattions
    
    ~params::  findone(self,filterkey=None)
        :- usesage doc.db.collection.findone(filterkey={"email":"example@eg.com"})

    ~params::  findall
        :- usesage doc.db.collection.findone(filterkey={"email":"example@eg.com"})

    ~params::  updatedoc
        :- usesage doc.db.collection.findone(filterkey={"email":"example@eg.com"})

    ~params::  deletedoc
        :- usesage doc.db.collection.findone(filterkey={"email":"example@eg.com"})
    
    connect                         - conenct to the database collection.
    insert(self,*addtodoc)          - Save the doccument
    findone                         - find one doc from the collection 
    findal                          - Find all doc if no specific key is provided
    update                          - update one existing doc
    delete                          - delete the doc provided 

    ##################
    global variables :-
    __connection__
    __schema__
    ##################
    """

    __connection__ = False
    __schema__ = None

    def __init__(self,*doc,**kw):
        super().__init__(*doc,**kw)
        self.__counter = 0
        self.__dbname = ""
        self.__collname = []
        
    def __getattr__(self,var):
        if self.__counter == 0:
            self.__dbname = var
        else:
            self.__collname.append(var)
        self.__counter +=1
        return self

    @classmethod
    def connect(cls,dburi="mongodb://localhost:27017/",username=None,password=None):
        try:
            cls.client =  pymongo.MongoClient(dburi)
            cls.__connection__ = True
        except Exception as e:
            raise ConnectionError (e)
        
    def insert(self,*addtodoc):
        # print(addtodoc)
        # print(self)
        self.update(*addtodoc)
        print(self)
        if self.__connection__ == True:
            if self.__schema__ is not None:
                print("validating")
                self.__verifySchema()
            try:
                collname = ".".join(self.__collname)
                print(self.__dbname, " ", collname)
                data = self.client[self.__dbname][collname].insert_one(self)
                self.__resetcounters()
                return data
            except pymongo.errors.DuplicateKeyError as e :
                self.__resetcounters()
                print(e)
                raise Errors.DuplicateKeyErr ("Doccument already present .Use update() instead")

        else:
            raise ConnectionError ("Mongo server not connected. user connect() befor operations")

        
    def findone(self,filterkey=None):
        collname = ".".join(self.__collname)
        if filterkey is not None:
            if isinstance(filterkey,dict):
                data = self.client[self.__dbname][collname].find_one(filterkey)
                self.__resetcounters()
                return data
            else:
                raise ValueError ("Incorrect filter object provided.should be Dict type")
        else:
            data = self.client[self.__dbname][collname].find_one(self)
            self.__resetcounters()
            return data
            
        

    def findall(self):
        pass

    def delete(self):
        pass

    def updateDoc(self):
        pass
    
    def __resetcounters(self):
        self.__counter *= 0
        self.__dbname *= 0
        self.__collname *= 0

    def __verifySchema(self,strictcheck=False):
        opt_count = 0
        for i in self.__schema__.items():
            # print(self.get(i[0]))
            print(i)
            if self.get(i[0]) is not None:
                # print(tuple(i[1]))
                if isinstance(self.get(i[0]),tuple(i[1])):
                    if PrimaryKey in tuple(i[1]):
                        self.__createindex(i[0])
                    print(i , " verified")
                else:
                    print(i)
                    raise Errors.SchemaError

            elif Optional in tuple(i[1]):
                opt_count +=1
            elif None in tuple(i[1]):
                continue
            else:
                raise Errors.SchemaError
        if len(self) != len(self.__schema__) - opt_count:
            # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            raise Errors.SchemaError

    def __createindex(self,index_name):
        collection =  ".".join(self.__collname)
        # print(self.__dbname, " ", collection ," ", index_name )
        # print("I am here ==========================")
        self.client[self.__dbname][collection].create_index([(index_name,pymongo.ASCENDING)],unique=True)