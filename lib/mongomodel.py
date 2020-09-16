# TODO :- class jsonSchemaModel() : -Implementations pending .refer to test.mongomodel.py file for info

#################
# Error classes #
#################

class Errors:

    class SchemaError(Exception):
        pass

    class DuplicateKeyErr(Exception):
        pass

    class InvalidDB(Exception):
        pass

##################################################
# Custome datatypes and Filed validation classes #
##################################################
from abc import ABC,abstractmethod
import re

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
        regex = "^[0-9a-zA-Z]*[.]?\w+[@]\w+[.a-zA-Z]+$"
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
            raise TypeError(value)

    def isoptional(self):
        # print(self.__optional)
        return self.__optional

    def canbeNull(self):
        return self.__canbenull
    
    def isunique(self):
        return self.__unique

###############################################
# main Model library classes wrapping pymongo #
###############################################
import pymongo
import inspect

class Model(type):
    def __new__(cls,name,base,dct):
        # print(cls,name,base,dct)
        if dct.get("__database__") is not None and dct.get("__collection__") is not None and dct.get("__schema__") is not None:
            if isinstance(dct.get("__schema__"),dict) and \
                            isinstance(dct.get("__database__"),str) and \
                            isinstance(dct.get("__collection__"),str):
                return super().__new__(cls,name,base,dct)
                
            else:
                raise AttributeError("verify {}:- \n\t\t\t __schema__ must be dictionary,\n\t\t\t __database__ must be str \n\t\t\t __collection__ must be str".format(name))
        else:
            raise AttributeError(f"mandatory values for {name} :- __database__ ,__collection__, __schema__")

class DocumentModel(dict,metaclass=Model):
    """ Verifyes and saves the schema model.This class needs to be inherited and the schema should be a list.
        It gives a doccument styte verification
        *******************
    Usesage/Example:- 

        exampleschema(Model):
            __database__ = "DBNAME"
            __collection__ = "colleciton_name"
            __schema__ = {
                "email_id":DocumentModel.fieldtype(Email,str,unique=True),
                "first_name":DocumentModel.fieldtype(str),
                "middle_name":DocumentModel.fieldtype(str,optional=True),
                "last_name":DocumentModel.fieldtype(str),
                "age":DocumentModel.fieldtype(int)
            }
        exampleschema.connect()     # connect to collection 
        doc = excampleschema({"documents":"detalis"})
        doc.insert()
        doc.findall() 

        *******************
    ##################
    Implemented methods:
    ##################
    ~params:: insert(self,*addtodoc) 
        :- usesage::- doc.insert() or doc.insert({"appened":"info to the main doc and save"})
    
    ~params:: connect(cls,dburi="mongodb://localhost:27017/",username=None,password=None))
        :- usesage .classmethod to connect to the db .Should be called before any oporattions
    
    ~params::  findone(self,filterkey=None)
        :- usesage doc.db.collection.findone(filterkey={"email":"example@eg.com"})
        :- returns a dictionary object or None if not present
           we can also use the schema Document model object to navigate the returned info
           
           EX:
                doc = schema(Documentmodel)
                doc.findone({"email":"w@ww.com"})
                doc.get("email") or doc["email"] = "new@mail.com"
            and directly can be saved like
                doc.insert() 

    ~params::  findall
        :- usesage doc.findone(filterkey={"email":"example@eg.com"})
        :- returns a list 

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
    __database__
    __collection__
    __schema__
    ##################
    """

    __connection= False
    __schema__ = dict()
    __database__ = str()
    __collection__ = str()
    # __getattr__ = dict.get
    # __setattr__ = dict.__setitem__
    # __delattr__ = dict.__delitem__


    # the below code will gather the db and coll info in obj.db.co.insert fassion()
    # def __init__(self,*doc,**kw):
    #     super().__init__(*doc,**kw)
    #     self.__counter = 0
    #     self.__dbname = ""
    #     self.__collname = []
        
    # def __getattr__(self,var):
    #     if self.__counter == 0:
    #         self.__dbname = var
    #     else:
    #         self.__collname.append(var)
    #     self.__counter +=1
    #     return self

    @classmethod
    def connect(cls,dburi="mongodb://localhost:27017/",username=None,password=None):
        try:
            cls.client =  pymongo.MongoClient(dburi)
            cls.__connection = True
        except Exception as e:
            raise ConnectionError (e)
        
    def insert(self,*addtodoc):
        # print(addtodoc)
        self.update(*addtodoc)
        print(self)
        if self.__connection == True:  
            print("validating")
            self.__verifySchema()
            try:
                print(self.__database__, ":=-", self.__collection__)
                data = self.client[self.__database__][self.__collection__].insert_one(self)
                print(data)
                return data

            except pymongo.errors.DuplicateKeyError as e :
                raise Errors.DuplicateKeyErr(e)

        else:
            raise ConnectionError ("Mongo server not connected. use connect() before operations")

        
    def findone(self,filterkey=None):
        if filterkey is not None:
            if isinstance(filterkey,dict):  
                data = self.client[self.__database__][self.__collection__].find_one(filterkey)
                print(data,self)
                if data is not None:
                    self.clear()
                    self.update(data)
                    return self
                else:
                    self.clear()
                    return data
            else:
                raise ValueError("Incorrect filter object provided.should be Dict type")
        else:
            data = self.client[self.__database__][self.__collection__].find_one(self)
            if data is not None:
                self.clear()
                self.update(data)
                return self
            else:
                return data


    def findall(self,*match:'optional filter dicitonary'):
        data = self.client[self.__database__][self.__collection__].find({},*match)
        return (x for x in data)


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


    def __verifySchema(self):
        opt_count = 0
        for fldkey, fldvalue in self.__schema__.items():
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
                    raise Errors.SchemaError("Scehma failed on entry {}".format((fldkey,e)))

            elif fldvalue.isoptional():
                opt_count +=1
            elif fldvalue.canbeNull():
                continue
            else:
                raise Errors.SchemaError("{} field not provided but defined".format(fldkey))
        if len(self) != len(self.__schema__) - opt_count:
            raise Errors.SchemaError("Unidentified field present in user data")

    def __createindex(self,index_name):
        try:
            self.client[self.__database__][self.__collection__].create_index([(index_name,pymongo.ASCENDING)],unique=True)
        except Exception as e:
            raise RuntimeError("failed while creating index for {} .{}".format(index_name,e))