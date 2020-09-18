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

class baseType(ABC):
    @abstractmethod
    def validatefield(self,value) -> bool:
        pass
    
class FieldType(baseType):
    # TODO can add more options based on database requirement
    def __init__(self,*args,**kwargs):
        print(kwargs)
        self.__definedtypes =[]
        self.__unique=kwargs.pop("unique",False)
        self.__optional=kwargs.pop("optional",False)
        self.__regex = kwargs.pop("regex")
        self.__custometype = None
        self.__canbenull=kwargs.pop("canbenull",False)
        
        if len(kwargs) !=0:
            raise AttributeError(f"unidentified values given {kwargs} for {self}") 
        
        for i in args:
            if inspect.isclass(i):
                if i in (str,int,bool,float,dict,list):
                    self.__definedtypes.append(i)
                elif i not in (frozenset,set,tuple) and self.__custometype is None:
                    self.__custometype = ielf.__definedtype
                else:
                    raise TypeError("Type \"{}\" is not acceptable/compatible ,\"{}\" ".format(i,self.__custometype))
            
            else:
                raise TypeError("Unidentified datatype \"{}\" in schema".format(i))
        self.checkobj()
        
    
    def validatefield(self,value)-> bool :
        if self.__custometype is not None:
            return self.__custometype().verify(value)

        elif isinstance(value,tuple(self.__definedtypes)):
            if self.__regex is not None:
                if re.search(self.__regex,value) is not True:
                    raise TypeError("{} regex dinot match")
            
            return True

        else:
            raise TypeError(f"type is {type(value)} defined :-{self.__definedtypes}")

    def isoptional(self):
        # print(self.__optional)
        return self.__optional

    def canbeNull(self):
        return self.__canbenull
    
    def isunique(self):
        return self.__unique

    def getregex(self):
        return self.__regex
    
    def checkobj(self):
        if isinstance(self.__unique,bool) != True or isinstance(self.__optional,bool) != True\
                                   or isinstance(self.__canbenull,bool) != True:
            raise RuntimeError("wrong format data given")
        elif isinstance(self.__regex,str):
            pass
        elif self.__regex is not None:
            raise RuntimeError("Wrong data regex")
        if self.__optional is True and self.__unique is True:
            raise RuntimeError(f"{self} value cannot be unique and optional")
        elif self.__unique is True and self.__canbenull is True:
            raise RuntimeError(f"{self} value cannot be unique and null/None")

class StringField(FieldType):
    def __init__(self,**kw):
        self.minimum = kw.pop("minimum",None)
        self.maximum = kw.pop("maximum",None)
        if self.minimum is not None and self.maximum is not None:
            if isinstance(self.minimum,int) is not True and isinstance(self.minimum,int) is not True:
                raise ValueError("min and max should be number")
            if self.minimum >= self.maximum or self.minimum == 0 or self.maximum == 0:
                raise ValueError("min and max values incorrect")
        super().__init__(**kw)
    
    def validatefield(self,value):
        if self.minimum is None and self.maximum is None:
            self.__checkdata(value)
            return True
        else:
            self.__checkdata(value)
            if self.minimum is not None and len(value) < self.minimum:
                raise TypeError(f"string {value} is under length")
            if self.maximum is not None and len(value) > self.maximum:
                raise TypeError(f"string {value} is over length")
            
            return True

    def __checkdata(self,val):
        
        if isinstance(val,str):  
            if self.getregex() is not None:
                if re.search(self.getregex(),val):
                    pass
                else:
                    raise TypeError(f"{val} donot mathch the regex field")
        elif self.canbeNull() is True:
            pass
        else:
            raise TypeError("value cannot be null/None")

class Email(FieldType):
    def validatefield(self,value):
        print("here")
        regex = self.getregex() or "^[0-9a-zA-Z]*[.]?\w+[@]\w+[.a-zA-Z]+$"
        print(regex)
        if re.search(regex,value):
            return True
        else:
            raise TypeError("{} is not a valid Email field".format(value))

class Date(FieldType):
    def __init__(self,**kw):
        pass

class Number(FieldType):
    def __inti__(self,**kw):
        self.minimum = kw.pop("minimum",None)
        self.maximum = kw.pop("maximum",None)
        if self.minimum is not None and self.maximum is not None:
            if isinstance(self.minimum,int) != True and isinstance(self.maximum,int) != True:
                raise ValueError("Invalid number")
            if self.minimum > self.maximum:
                raise ValueError(f"{self.minimum} cannot be greater than {self.maximum}")
        super().__init__(**kw)
    
    def validatefield(self,value):
        if isinstance(value,int) is not True:
            raise TypeError(f"{value} is not a number")
        if self.minimum is not None and self.maximum is not None:
            if value < self.minimum:
                raise ValueError(f"{value} not meeting the defined min")
            if value > self.maximum:
                raise ValueError(f"{value} exceding the defined max")
        return True



        
###############################################
# main Model library classes wrapping pymongo #
###############################################
import pymongo
import inspect

class Model(type):
    def __new__(cls,name,base,dct):
        # print(cls,name,base,dct)
        if isinstance(dct.get("__database__"),str) and len(dct.get("__database__")) != 0 \
                and isinstance(dct.get("__collection__"),str) and len(dct.get("__collection__")) != 0:
            if dct.get("__schema__") is None:
                return super().__new__(cls,name,base,dct)

            if isinstance(dct.get("__schema__"),dict) and len(dct.get("__schema__")) != 0:
                for key,value in dct.get("__schema__").items():
                    print(key,value)
                    if isinstance(value,FieldType):
                        pass
                    elif isinstance(value,(dict,list)) and len(value) != 0:
                        cls.verifydefinition(value)
                    else:
                        raise AttributeError(f"failed at {key} value {value} is of {type(value)} accepts <class FieldType>,non empty <dict> or <list>")                
                return super().__new__(cls,name,base,dct)
                
            else:
                raise AttributeError(f"verify {name}:- \n\t\t\t __schema__ must be a dictionary or None")
        else:
            raise AttributeError(f"mandatory class variables for {name} :-\n__database__ <class str> ,\n__collection__ <class str>, \n__schema__ <class dict> or None")

    @classmethod
    def verifydefinition(cls,values):
        if isinstance(values,dict):
            for k,v in values.items():
                if isinstance(v,dict) and len(v) != 0:
                    cls.verifydefinition(v)
                elif isinstance(v,list) and len(v) != 0:
                    cls.verifydefinition(v)
                elif isinstance(v,FieldType):
                    pass
                else:
                    raise AttributeError(f"wrong datatype at {k} ,{v} ,use <class FieldType> ,cannot be empty dict() or str()")
        if isinstance(values,list):
            for i in values:
                if isinstance(i,dict) and len(i) != 0:
                    cls.verifydefinition(i)
                elif isinstance(i,list) and len(i) != 0:
                    cls.verifydefinition(i)
                elif isinstance(i,FieldType):
                    pass
                else:
                    raise AttributeError(f"wrong datatype at {i},use <class FieldType> ,cannot be empty dict() or str()")
        
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
            if self.__schema__ is not None:
                print("validating")
                DocumentModel.verifyschema(self.__schema__,self)
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
    
    def count(self):
        pass
    
    @staticmethod
    def fieldtype(*args,unique=False,canbenull=False,optional=False,regex=None):
        if isinstance(unique,bool) and isinstance(optional,bool):
            return FieldType(*args,unique=unique,canbenull=canbenull,optional=optional,regex=regex)
        else:
            raise TypeError("keyword unique and optional values should be of boolean type and regex is str")

    @staticmethod
    def verifyschema(schema_data,data):
        opt_count = 0
        for skey,svalue in schema_data.items():
            # print(skey,svalue)
            if data.get(skey) is not None:
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
                raise Errors.SchemaError(f"{skey} cannot have empty values")
            elif svalue.isoptional():
                opt_count +=1
            elif svalue.canbeNull():
                continue
            else:
                print(data.get(skey) ,skey,data,"  this is ")
                raise Errors.SchemaError("{} field not provided but defined".format(skey))

        if len(data) != len(schema_data) - opt_count:
            raise Errors.SchemaError(f"Schema params didnot match incoming data,[+] defined schema {schema_data}")
    
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
            if isinstance(ivalue,FieldType) and ivalue.isunique() == True:
                try:
                    print("creating primary index for {}".format(ikey))
                    self.client[self.__database__][self.__collection__].create_index([(ikey,pymongo.ASCENDING)],unique=True)
                except Exception as e:
                    raise RuntimeError("failed while creating index for {} .{}".format(ikey,e))