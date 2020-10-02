# TODO :- class jsonSchemaModel() : -Implementations pending .refer to test.mongomodel.py file for info
        
###############################################
# main Model library classes wrapping pymongo #
###############################################
import pymongo
from .baseclasses import Model,baseType,EmbeddedDocbase
from .tools import verifyschema
from .datatypes import FieldType
from . import Errors

class DocumentModel(dict,metaclass=Model):
    """ Verifyes and saves the schema model.This class needs to be inherited and the schema should be a list.
        It gives a doccument styte verification
        *******************
    Usesage/Example:- 

        exampleschema(DocumentModel):
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
        :- usesage doc.findall(filterkey={"email":"example@eg.com"})
        :- returns a list

    ~params::  updatedoc
        :- usesage doc.updatedoc(filterkey={"email":"example@eg.com"})

    ~params::  deletedoc
        :- usesage doc.deletedoc(filterkey={"email":"example@eg.com"})
    ##################
    global variables :-
    __database__
    __collection__
    __schema__
    ##################
    """

    __connection= False
    __schema__ = None
    __database__ = "test_db"
    __collection__ = "test_collection"

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
            if self.__schema__ is not None:
                print("validating")
                verifyschema(self.__schema__,self)
                print(self)
                self.__createindex()
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
        if self.__connection != True:
            raise ConnectionError("Mongo server not conencted user connect() before operations")
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
        if self.__connection != True:
            raise ConnectionError("Mongo server not conencted user connect() before operations")
        data = self.client[self.__database__][self.__collection__].find({},*match)
        return (x for x in data)


    def delete(self):
        if self.__connection != True:
            raise ConnectionError("Mongo server not conencted user connect() before operations")
        pass

    def updateDoc(self):
        if self.__connection != True:
            raise ConnectionError("Mongo server not conencted user connect() before operations")
        pass
    
    def count(self):
        if self.__connection != True:
            raise ConnectionError("Mongo server not conencted user connect() before operations")
        pass


    def __createindex(self):
        if self.__connection != True:
            raise ConnectionError("Mongo server not conencted user connect() before operations")
        for ikey,ivalue in self.__schema__.items():
            if isinstance(ivalue,baseType) and ivalue.isunique() == True:
                try:
                    print("creating primary index for {}".format(ikey))
                    self.client[self.__database__][self.__collection__].create_index([(ikey,pymongo.ASCENDING)],unique=True)
                except Exception as e:
                    raise RuntimeError("failed while creating index for {} .{}".format(ikey,e))

    @staticmethod
    def fieldtype(*args,**k):
        if len(args) == 0:
            raise RuntimeError("arguments cannot be empty")
        return FieldType(*args,**k)

