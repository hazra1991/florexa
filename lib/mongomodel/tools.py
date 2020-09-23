from . import Errors

def verifyschema(schema_data,data):
    opt_count = 0
    for skey,svalue in schema_data.items():
        # print(skey,svalue)
        if data.get(skey) is not None:
            if isinstance(svalue,dict):
                if isinstance(data.get(skey),dict):
                    print("entered dict")
                    verifyschema(svalue,data.get(skey))
                else:
                    raise Errors.SchemaError(f"Schema at {skey} defined as {type(svalue)} but provided {type(data.get(skey))}")

            elif isinstance(svalue,list):
                __listverify(svalue,data.get(skey),skey)
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
                        raise Errors.SchemaError("schema error somethng went wrong.,validatefield returned None")
                except TypeError as e:
                    raise Errors.SchemaError("Scehma failed on entry {}".format((skey,e)))
                        #validation
        elif isinstance(svalue,dict) or isinstance(svalue,list):
            raise Errors.SchemaError(f"{skey} cannot have empty values")
        elif hasattr(svalue,'default') and svalue.default != None:
            if callable(svalue.default):
                _v = svalue.default()
                if isinstance(_v,(str,int)):
                    data[skey] = _v
                else:
                    data[skey] =str(_v)
            else:
                data[skey]= svalue.default
        elif svalue.isoptional():
            opt_count +=1
        elif svalue.canbeNull():
            try:
                data[skey]
            except KeyError:
                raise Errors.SchemaError(f"{skey} is defined but not provided")
        else:
            print(data.get(skey) ,skey,data)
            raise Errors.SchemaError("{} field not provided but defined".format(skey))

    if len(data) != len(schema_data) - opt_count:
        raise Errors.SchemaError(f"Schema params didnot match incoming data,[+] defined schema {schema_data}")

def __listverify(lstvalue,pdata,key):
    if isinstance(pdata,list):
        if len(lstvalue) != len(pdata):
            raise Errors.SchemaError(f"provided data for \"{key}\" = {pdata} index missmatch [+]list cannot have optional values [+] use fieldtype(list) for emty list")
        for i in range(len(lstvalue)):
            if isinstance(lstvalue[i],dict):
                if isinstance(pdata[i],dict):
                    verifyschema(lstvalue[i],pdata[i])
                    print("cameback from dict")
                else:
                    raise Errors.SchemaError(f"Failed on {key} data defined {lstvalue[i]} given {pdata[i]} ")
            elif isinstance(lstvalue[i],list):
                if isinstance(pdata[i],list):
                    __listverify(lstvalue[i],pdata[i],key)
                else:
                    raise Errors.SchemaError(f"Failed on {key} data defined {lstvalue[i]} given {pdata[i]} ")
            else :

                print(f"schema for list {key} is {lstvalue[i]} and data value is {pdata[i]}")
                try:
                    if lstvalue[i].validatefield(pdata[i]) == True:
                        pass
                    else:
                        print((key , lstvalue[i])," : -- failed")
                        raise Errors.SchemaError("schema error somethng went wrong,validatefield returned None")
                except TypeError as e:
                    raise Errors.SchemaError("Scehma failed on entry {}".format((key,e)))
                
    else:
        raise Errors.SchemaError(f"Scehma failed on entry {key} defined {type(lstvalue)} but given{type(pdata)}")