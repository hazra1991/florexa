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

        **Not recomened:-
                | - > doc.dbname.collectionname.insert() or doc.dbname.collectionname.findone()**

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
    __database__ = None
    __collection__ = None

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
            else:
                raise Errors.SchemaError("collection Schema not defined")
            try:
                if self.__database__ is not None and self.__collection__ is not None:
                    print(self.__database__, ":=-", self.__collection__)
                    data = self.client[self.__database__][self.__collection__].insert_one(self)
                    self.__resetcounters()
                    return data
                elif self.__dbname != "":
                    collname = ".".join(self.__collname)
                    print(self.__dbname, ":=-", collname)
                    data = self.client[self.__dbname][collname].insert_one(self)
                    self.__resetcounters()
                    return data
                else:
                    raise InvalidDB("DB or collection not given")
        
            except pymongo.errors.DuplicateKeyError as e :
                self.__resetcounters()
                raise Errors.DuplicateKeyErr(e)

        else:
            raise ConnectionError ("Mongo server not connected. user connect() befor operations")

        
    def findone(self,filterkey=None):
        collname = ".".join(self.__collname)
        if filterkey is not None:
            if isinstance(filterkey,dict):
                if self.__database__ is not None and self.__collection__ is not None:
                    data = self.client[self.__database__][self.__collection__].find_one(filterkey)
                    return data
                else:
                    data = self.client[self.__dbname][collname].find_one(filterkey)
                    self.__resetcounters()
                    return data
            else:
                raise ValueError("Incorrect filter object provided.should be Dict type")
        else:
            if self.__database__ is not None and self.__collection__ is not None:
                data = self.client[self.__database__][self.__collection__].find_one(self)
                return data
            else:
                data = self.client[self.__dbname][collname].find_one(self)
                self.__resetcounters()
                return data
            
        

    def findall(self):
        if self.__database__ is not None and self.__collection__ is not None:
            data = self.client[self.__database__][self.__collection__].find({})
            return [x for x in data]
        else:
            collname = ".".join(self.__collname)
            data = self.client[self.__dbname][collname].find({})
            self.__resetcounters()
            return [x for x in data]


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
                    raise Errors.SchemaError("Scehma failed on entry {}".format((fldkey,e)))

            elif fldvalue.isoptional():
                opt_count +=1
            elif fldvalue.canbeNull():
                continue
            else:
                raise Errors.SchemaError("{} field not provided but defined".format(fldkey))
        if len(self) != len(self.__schema__) - opt_count:
            # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            raise Errors.SchemaError("Unidentified field present in user data")

    def __createindex(self,index_name):
        # print(self.__dbname, " ", collection ," ", index_name )
        # print("I am here ==========================")
        if self.__dbname != "":
            collection =  ".".join(self.__collname)
            self.client[self.__dbname][collection].create_index([(index_name,pymongo.ASCENDING)],unique=True)
        elif self.__database__ is not None and self.__collection__ is not None:
            self.client[self.__database__][self.__collection__].create_index([(index_name,pymongo.ASCENDING)],unique=True)


# ------------------------------
# Here is the example model
# ------------------------------        

class UserSchema(DocumentModel):
    __schema__ = {
        "email_id":[str,PrimaryKey],
        "first_name":[str],
        "middle_name":[str,None],
        "last_name":[str],
        "password":[str],
        "phone":[int],
        "location":[str,Optional],
        "verifyed":[bool],
        "verified_on":[str,None],
        "DOB":[str]
    }

######################
# inserting document #
######################

UserSchema.connect()
document =  UserSchema({"email_id":"dsdsddd",
        "first_name":"abhisehk",
        "middle_name":None,
        "last_name":"str",
        "password":"str",
        "phone":9999999999,
        "location":"str",
        "verifyed":False,
        "verified_on":"None",
        "DOB":"str"
        })


# document.florexa.user_info.insert()
print(document.florexa.user_info.s.d.s.findone({"email_id":"89898989"}))
document.florexa.user_info.s.d.s.insert()

# print(document.__all__)

exit()

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