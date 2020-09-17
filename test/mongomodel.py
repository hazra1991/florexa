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
    def __init__(self,*args,unique=False,optional=False,canbenull=False,regex=None):
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
                # raise exception here 
            
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
# dummydb
# dummy_collection
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
            DocumentModel.verifyschema(self.__schema__,self)
            try:
                print(self.__database__, ":=-", self.__collection__)
                # data = self.client[self.__database__][self.__collection__].insert_one(self)
                # print(data)
                # return data

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
            raise TypeError("keyword unique and optional values should be of boolean type and regex is str")
   
    @staticmethod
    def verifyschema(schema_data,data):
        opt_count = 0
        for skey,svalue in schema_data.items():
            print(skey,svalue)
            if data.get(skey) is not None:
                print(skey,svalue)
                if isinstance(svalue,dict):
                    if isinstance(data.get(skey),dict):
                        print("entered dict")
                        DocumentModel.verifyschema(svalue,data.get(skey))
                    else:
                        raise Errors.SchemaError(f"Schema at {skey} defined as {type(svalue)} but provided {type(data.get(skey))}")

                elif isinstance(svalue,list):
                    DocumentModel.__listverify(svalue,data.get(skey),skey)
                else:
        
                    print(f"validating schema for {skey} and type {svalue} with data {data.get(skey)}")
                    try:
                        if svalue.validatefield(data.get(skey)) == True:
                            if svalue.isunique() == True:
                                # self.__createindex(fldkey)
                                pass
                            print((skey , svalue) , " verified")
                        else:
                            print((skey , svalue)," : -- failed")
                            raise Errors.SchemaError("schema error somethng went wrong")
                    except TypeError as e:
                        raise Errors.SchemaError("Scehma failed on entry {}".format((skey,e)))
                            #validation
            elif isinstance(svalue,dict) or isinstance(svalue,list):
                raise Errors.SchemaError(f"{skey} field not provided but defined")
            elif svalue.isoptional():
                opt_count +=1
            elif svalue.canbeNull():
                continue
            else:
                raise Errors.SchemaError("{} field not provided but defined".format(skey))

        if len(data) != len(schema_data) - opt_count:
            raise Errors.SchemaError("Unidentified field present in user data")      
    @staticmethod
    def __listverify(lstvalue,pdata,key):
        if isinstance(pdata,list):
            if len(lstvalue) != len(pdata):
                raise Errors.SchemaError(f"provided data for \"{key}\" = {pdata} index missmatch [+]list cannot have optional values [+] use fieldtype(list) for emty list")
            for i in range(len(lstvalue)):
                if isinstance(lstvalue[i],dict):
                    if isinstance(pdata[i],dict):
                        DocumentModel.verifyschema(lstvalue[i],pdata[i])
                        print("cameback from dict")
                    else:
                        raise Errors.SchemaError(f"Failed on {key} data defined {lstvalue[i]} given {pdata[i]} ")
                elif isinstance(lstvalue[i],list):
                    if isinstance(pdata[i],list):
                        DocumentModel.__listverify(lstvalue[i],pdata[i],key)
                    else:
                        raise Errors.SchemaError(f"Failed on {key} data defined {lstvalue[i]} given {pdata[i]} ")
                else :

                    print(f"schema for list {key} is {lstvalue[i]} and data value is {pdata[i]}")
                    try:
                        if lstvalue[i].validatefield(pdata[i]) == True:
                            pass
                        else:
                            print((key , lstvalue[i])," : -- failed")
                            raise Errors.SchemaError("schema error somethng went wrong")
                    except TypeError as e:
                        raise Errors.SchemaError("Scehma failed on entry {}".format((key,e)))
                    
        else:
            raise Errors.SchemaError(f"Scehma failed on entry {key} defined {type(lstvalue)} but given{type(pdata)}")

    def __createindex(self):
        for ikey,ivalue in self.__schema__.items():
            if isinstance(ivalue,FiledType) and ivalue.isunique() == True:
                try:
                    self.client[self.__database__][self.__collection__].create_index([(index_name,pymongo.ASCENDING)],unique=True)
                except Exception as e:
                    raise RuntimeError("failed while creating index for {} .{}".format(ikey,e))

class UserSchema(DocumentModel):
    __database__ ="florexa"
    __collection__="user_info"
    __schema__ = {
        # "email_id":DocumentModel.fieldtype(Email,str,unique=True),
        "first_name":DocumentModel.fieldtype(None),
        # "middle_name":DocumentModel.fieldtype(str,optional=False),
        # "last_name":DocumentModel.fieldtype(str),
        # "password":DocumentModel.fieldtype(str),
        # "phone":DocumentModel.fieldtype(int),
        # "location":DocumentModel.fieldtype(str,optional=False),
        # "verifyed":DocumentModel.fieldtype(bool),
        # "verified_on":DocumentModel.fieldtype(str,int),
        "DOB":{
            "name":{
                "fst":DocumentModel.fieldtype(str,optional=True),
                "new":[{"inside":DocumentModel.fieldtype(str,optional=False)}]
            }
        }
    }

doc = UserSchema({"first_name":None,"DOB":{"name":{"new":[{"inside":"12","another":"ihi"}]}}})

doc.connect()
doc.insert()

#################################################

#----- Different aproach (doing validation in DB)

#################################################

class jsonSchemaModel():
    """Need to Implement another way of validating based onthe below json scema 
    and this link:-https://stackoverflow.com/questions/61074297/how-to-create-schema-in-mongodb-using-python
    """
# https://stackoverflow.com/questions/61074297/how-to-create-schema-in-mongodb-using-python
    pass

# from pymongo import MongoClient
# from collections import OrderedDict
# import sys

# client = MongoClient()   # supply connection args as appropriate 
# db = client.testX

# db.myColl.drop()

# db.create_collection("myColl")  # Force create!

# #  $jsonSchema expression type is prefered.  New since v3.6 (2017):
# vexpr = {"$jsonSchema":
#   {
#          "bsonType": "object",
#          "required": [ "name", "year", "major", "gpa" ],
#          "properties": {
#             "name": {
#                "bsonType": "string",
#                "description": "must be a string and is required"
#             },
#             "gender": {
#                "bsonType": "string",
#                "description": "must be a string and is not required"
#             },
#             "year": {
#                "bsonType": "int",
#                "minimum": 2017,
#                "maximum": 3017,
#                "exclusiveMaximum": False,
#                "description": "must be an integer in [ 2017, 3017 ] and is required"
#             },
#             "major": {
#                "enum": [ "Math", "English", "Computer Science", "History", None ],
#                "description": "can only be one of the enum values and is required"
#             },
#             "gpa": {
#                "bsonType": [ "double" ],
#                "minimum": 0,
#                "description": "must be a double and is required"
#             }
#          }
#   }
# }

# cmd = OrderedDict([('collMod', 'myColl'),
#         ('validator', vexpr),
#         ('validationLevel', 'moderate')])

# db.command(cmd)

# try:
#     db.myColl.insert({"x":1})
#     print "NOT good; the insert above should have failed."
# except:
#     print "OK. Expected exception:", sys.exc_info()    

# try:
#     okdoc = {"name":"buzz", "year":2019, "major":"Math", "gpa":3.8}
#     db.myColl.insert(okdoc)
#     print "All good."
# except:
#     print "exc:", sys.exc_info()