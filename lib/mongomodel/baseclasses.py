import inspect
from abc import ABC,abstractmethod

def verifydefinition(values,classname=None):
    if isinstance(values,dict):
        for k,v in values.items():
            if isinstance(v,dict) and len(v) != 0:
                verifydefinition(v)
            elif isinstance(v,list) and len(v) != 0:
                verifydefinition(v)
            elif isinstance(v,baseType):
                pass
            else:
                raise AttributeError(f"{classname} wrong datatype at {k} ,{v} ,need non empty {dict} ,{list} or defined in datatypes")
    if isinstance(values,list):
        for i in values:
            if isinstance(i,dict) and len(i) != 0:
                verifydefinition(i)
            elif isinstance(i,list) and len(i) != 0:
                verifydefinition(i)
            elif isinstance(i,baseType):
                pass
            else:
                raise AttributeError(f"{classname} wrong datatype at {i},need non empty {dict} ,{list} or defined in datatypes")

class baseType(ABC):
    def __init__(self,*args,**kwargs):
        self.__definedtypes =[]
        self.__unique=kwargs.pop("unique",False)
        self.__optional=kwargs.pop("optional",False)
        self.__canbenull=kwargs.pop("canbenull",False)
        print(args)
        
        if len(kwargs) !=0:
            raise AttributeError(f"unidentified values given {kwargs} for {self}") 
        
        for i in args:
            if inspect.isclass(i):
                if i in (str,int,bool,float,dict,list):
                    self.__definedtypes.append(i)
                else:
                    raise TypeError("Type \"{}\" is not acceptable ,\"{}\" ".format(i,self.__custometype))
            
            else:
                raise TypeError("Unidentified datatype \"{}\" in schema".format(i))
        self.checkobj()

    def isoptional(self):
        return self.__optional

    def canbeNull(self):
        return self.__canbenull
    
    def isunique(self):
        return self.__unique
        
    def getdefinedtypes(self):
        return self.__definedtypes
    
    def checkobj(self):
        if isinstance(self.__unique,bool) != True or isinstance(self.__optional,bool) != True\
                                   or isinstance(self.__canbenull,bool) != True:
            raise RuntimeError("wrong format data given")

        if self.__optional is True and self.__unique is True:
            raise RuntimeError(f"{self} value cannot be unique and optional")
        elif self.__unique is True and self.__canbenull is True:
            raise RuntimeError(f"{self} value cannot be unique and null/None")
        elif self.__canbenull is True and self.__optional is True:
            raise RuntimeError(f"{self} values can be either optional or null")

    @abstractmethod
    def validatefield(self,value) -> bool:
        pass

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
                    if isinstance(value,baseType):
                        pass
                    elif isinstance(value,(dict,list)) and len(value) != 0:
                        verifydefinition(value,classname=name)
                    else:
                        raise AttributeError(f"{name}failed at {key} value {value} is of {type(value)},expected {dict} or {baseType}")                
                return super().__new__(cls,name,base,dct)
                
            else:
                raise AttributeError(f"verify {name}:- \n\t\t\t __schema__ must be a dictionary or None")
        else:
            raise AttributeError(f"mandatory class variables for {name} :-\n__database__ <class str> ,\n__collection__ <class str>, \n__schema__ <class dict> or None")

class EmbeddedDocbase(type):
    def __new__(cls,name,base,dct):
        if dct.get("__schema__") is not None and isinstance(dct.get("__schema__"),dict):
            verifydefinition(dct.get("__schema__"),classname=name)
        else:
            raise AttributeError("__schema__ variable cannot be empty and should {dict} ")

        return super().__new__(cls,name,base,dct)


