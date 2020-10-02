import re
from .baseclasses import baseType,verifydefinition
from .tools import verifyschema

class FieldType(baseType):
    # TODO can add more options based on database requirement
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__definedtype = self.getdefinedtypes()
        
    
    def validatefield(self,value):
        if isinstance(value,tuple(self.__definedtype)):
            return True
        else:
            raise TypeError(f"type is {type(value)} defined :-{self.__definedtype}")

class StringField(baseType):
    def __init__(self,**kw):
        self.minimum = kw.pop("minimum",None)
        self.maximum = kw.pop("maximum",None)
        self.default = kw.pop("default",None)
        self.regex = kw.pop("regex",None)
        if self.default is not None:
            if isinstance(self.default,str) or callable(self.default):
                pass
            else:
                raise RuntimeError("wrong default value set")
        if self.minimum is not None and isinstance(self.minimum,int):
            raise ValueError("invalid minimum value")
        if self.maximum is not None and isinstance(slef.maximum,int):
            raise ValueError("Invalid maximum")
        try:
            if self.minimum > self.maximum:
                raise ValueError(f"{self.minimum} cannot be greater than {self.maximum}")
        except TypeError:
            pass
        if self.regex == None or isinstance(self.regex,str):
            pass

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
            if self.regex is not None:
                if re.search(self.regex,val):
                    pass
                else:
                    raise TypeError(f"{val} donot mathch the regex field")
        elif self.canbeNull() is True and val is None:
            pass
        else:
            raise TypeError(f"{val} defined {str} , givem {type(val)}")

class Email(baseType):
    def __init__(self,**kw):
        self.regex = kw.pop("regex",None)
        super().__init__(**kw)

    def validatefield(self,value):
        print("here")
        regex = self.regex or "^[0-9a-zA-Z]*[.]?\w+[@]\w+[.a-zA-Z]+$"
        if re.search(regex,value):
            return True
        else:
            raise TypeError("{} is not a valid Email field".format(value))

class DateTime(baseType):
    from datetime import datetime
    def __init__(self,**kw):
        self.default = kw.pop("default",None)
        self.unixtime = kw.pop("unixtime",False)
        self.format = kw.pop("_format","%d/%m/%Y")
        
        if isinstance(self.format,str) is not True:
            raise ValueError(f"{self.format} should be a string")
        if isinstance(self.unixtime,(int,float)) != True:
            raise RuntimeError("unixtime should be ")

        if self.default == None or callable(self.default): 
            pass
        else:
            raise RuntimeError("default should be a Datetime object")
        super().__init__(**kw)
    
    def validatefield(self,value):
        # TODO need to implememt unix timestamp
        if isinstance(value,str):
            datetime.strptime(value,self.format)
        else:
            raise ValueError(f"{value} date object should be a string in format {self.format}")
            


class NumberField(baseType):
    def __init__(self,**kw):
        self.minimum = kw.pop("minimum",None)
        self.maximum = kw.pop("maximum",None)
        self.default = kw.pop("default",None)

        if self.default != None and isinstance(self.default,int) is not True: 
            raise RuntimeError(f"default {self.default} not a number")

        if self.minimum is not None and isinstance(self.minimum,int) is not True:
            raise ValueError("invalid minimum value")
        if self.maximum is not None and isinstance(self.maximum,int) is not True:
            raise ValueError("Invalid maximum")
        try:
            if self.minimum > self.maximum:
                raise ValueError(f"{self.minimum} cannot be greater than {self.maximum}")
        except TypeError:
            pass
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

class EmbeddedDocumentList(baseType):
    def __init__(self,embdoc,**kw):
        self.embdoc = embdoc
        if kw.get("unique") or kw.get("optional"):
            raise RuntimeError("Embaded lists cannot be unique or optional")
        if isinstance(embdoc,dict) is not True:
            raise RuntimeError(f"{embdoc} should be a dictionary")
        verifydefinition(embdoc,classname="Embedded doc")
        super().__init__(**kw)

        print(embdoc)
        
    def validatefield(self,value):
        if isinstance(value,list) is not True:
            raise TypeError(f"{value} is not a valid list")
        if len(value) ==0:
            raise TypeError("Embbeded list cannot have empty values")
        for i in value:
            if isinstance(i,dict):
                verifyschema(self.embdoc,i)
            else:
                raise TypeError(f"{i} should be a dict in {value}")
            
        return True

class Boolean(baseType):
    def __init__(self,**kw):
        self.default = kw.pop("default",None)
        if self.default != None and isinstance(self.default,bool) != True:
            raise ValueErro("default should be a bool")
        super().__init__(**kw)

    def validatefield(self,value):
        if isinstance(value,bool):
            return True
        else:
            raise TypeError(f"{value} value is not a bool")