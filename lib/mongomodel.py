# TODO :- class jsonSchemaModel() : -Implementations pending .refer to test.mongomodel.py file for info

import pymongo
from abc import ABC,abstractmethod
import re,inspect
class Errors:

    class SchemaError(Exception):
        pass

    class DuplicateKeyErr(Exception):
        pass
    
class CustomeDataType(ABC):
    @abstractmethod
    def verify(self):
        pass


# class Date(CustomeDataType):
    
#     # TODO 
#     """ need to create a custome date datatype """
#     def __init__(self,format=""):
#         pass
#     def verify
#     pass
class Email(CustomeDataType):
    def verify(self,value):
        regex = "^[0-9a-zA-Z]+[._]?\w+[@]\w+[.a-zA-Z]+$"
        if re.search(regex,value):
            return True
        else:
            raise TypeError("{} is not a valid Email field".format(value))
    

class FiledType:
    # TODO can add more options based on database requirement
    def __init__(self,*args,unique=False,optional=False,regex=None):
        self.__definedtypes =[]
        self.__unique=unique
        self.__optional=optional
        self.__regex = regex
        self.__custometype = None
        self.__canbenull=False

        for i in args:
            if inspect.isclass(i):
                if i in (str,int,bool,float,dict,list):
                    self.__definedtypes.append(i)
                elif i not in (frozenset,set,tuple) and self.__custometype is None:
                    self.__custometype = i
                else:
                    raise TypeError("Type \"{}\" is not compatible with tye \"{}\" ".format(i,self.__custometype))
            elif i is None:
                self.__canbenull = True
            
            else:
                raise TypeError("Unidentified datatype \"{}\" in schema".format(i))
        
    
    def validatefield(self,value):
        if self.__custometype is not None:
            return self.__custometype().verify(value)

        elif isinstance(value,tuple(self.__definedtypes)):
            if self.__regex is not None:
                if re.search(self.__regex,value) is not True:
                    raise TypeError("{} regex dinot match")
            
            return True

        else:
            raise TypeError("datatype for {} didnot match".format(value))

    def isoptional(self):
        print(self.__optional)
        return self.__optional

    def canbeNull(self):
        return self.__canbenull
    
    def isunique(self):
        return self.__unique

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
                "email_id":DocumentModel.fieldtype(Email,str,unique=True),
                "first_name":DocumentModel.fieldtype(str),
                "middle_name":DocumentModel.fieldtype(str,optional=True),
                "last_name":DocumentModel.fieldtype(str),
                "age":DocumentModel.fieldtype(int)
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
                raise Errors.DuplicateKeyErr(e)

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
                raise ValueError("Incorrect filter object provided.should be Dict type")
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
    
    @staticmethod
    def fieldtype(*args,unique=False,optional=False,regex=None):
        if isinstance(unique,bool) and isinstance(optional,bool):
            return FiledType(*args,unique=unique,optional=optional,regex=regex)
        else:
            raise TypeError("keyword values should be of boolean type")
        
        

    def __resetcounters(self):
        self.__counter *= 0
        self.__dbname *= 0
        self.__collname *= 0

    def __verifySchema(self):
        opt_count = 0
        for fldkey, fldvalue in self.__schema__.items():
            # print(self.get(i[0]))
            # print(fldkey)
            if self.get(fldkey) is not None:
                try:
                    if fldvalue.validatefield(self.get(fldkey)) == True:
                        if fldvalue.isunique() == True:
                            self.__createindex(fldkey)
                        print((fldkey , fldvalue) , " verified")
                    else:
                        print((fldkey , fldvalue)," : -- failed")
                        raise Errors.SchemaError("schema error somethng went wrong")
                except TypeError as e:
                    raise Errors.SchemaError(e)

            elif fldvalue.isoptional():
                opt_count +=1
            elif fldvalue.canbeNull():
                continue
            else:
                raise Errors.SchemaError("{} field not provided but defined".format(fldkey))
        if len(self) != len(self.__schema__) - opt_count:
            # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            raise Errors.SchemaError

    def __createindex(self,index_name):
        collection =  ".".join(self.__collname)
        # print(self.__dbname, " ", collection ," ", index_name )
        # print("I am here ==========================")
        self.client[self.__dbname][collection].create_index([(index_name,pymongo.ASCENDING)],unique=True)