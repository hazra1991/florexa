# data = {
#     "name":"some name",
#     "age":23,
#     "hoby":[
#                     {
#                     "singing":{"rating":2,"how":"not good"}},
#                {
#                    "dancing":{
#                        "rating":2,"how":"not good"
#                    }
#                } ],
#     "others":{
#         "dontknow":"dummydata",
#         "dummydict":"dummydictdata",
#         "newvariable":[1,3,4,{"somemoredict":[543,534,35,345]},5,6]
#     }
#     }

schema = {
    "name":str,
    "age":int,
    "hoby":[{
                    "singing":{"rating":int,"how":str}},
               {
                   "dancing":{
                       "rating":int,"how":str
                   }
               } ],
    "others":{
        "dontknow":str,
        "dummydict":str,
        "newvariable":[int,int,int,{"somemoredict":list},int,int]
    }
    }

# need to change the schema to none and list or dict cannot be 0 in meta 

# "hoby":[0,"singing","raiting","how",1,""]
# print(len(data),len(schema))
# import time
# def verifyschema(schema_data,data,path=""):
#     for skey,svalue in schema_data.items():
#         if data.get(skey) is not None:
#             if isinstance(svalue,dict):
#                 if isinstance(data.get(skey),dict):
#                     print("entered dict")
#                     verifyschema(svalue,data.get(skey))
#                 else:
#                     print("failed")

#             elif isinstance(svalue,list):
#                 listverify(svalue,data.get(skey),skey)
#             else:
#                 time.sleep(2)         
#                 print(f"schema for {skey} is {svalue} and data value is {data.get(skey)}")
#                 #validation
            

# def listverify(lstvalue,pdata,key):
#     if isinstance(pdata,list):
#         for i in range(len(lstvalue)):
#             if isinstance(lstvalue[i],dict):
#                 if isinstance(pdata[i],dict):
#                     verifyschema(lstvalue[i],pdata[i])
#                     print("cameback from dict")
#                 else:
#                     print("failed chekck")
#             elif isinstance(lstvalue[i],list):
#                 if isinstance(pdata[i],list):
#                     listverify(lstvalue[i],pdata[i])
#                 else:
#                     print("failed check lis")
#             else :
#                 time.sleep(2)
#                 print(f"schema for list {key} is {lstvalue[i]} and data value is {pdata[i]}")

#     else:
#         print("failed list check")
      
      
      
      
      
      
        # do stuff
        # verifyschema({svalue},data[skey])
            
            # if isinstance(schema_data,list) and isinstance(data,list):
            #     for i in schema_data:
            #         if isinstance(i,dict):
            #             verifyschema(i)
            #         elif isinstance(i,list):
            #             verifyschema(i)
            #         else:
            #             print(f"list value is {i}")


# verifyschema(schema,data)

# for skey,svalue in schema.items():
#     if data.get(key) is not None:
#         if isinstance(svalue,(dict,list)) and isinstance(data[key],(dict,list)):
#             verifyschema(svalue,data[key])   # pass the self data also for this key 
#         else:
#             print(f"key is :-- {key},value is {value}")


# verifyschema(data)

            


# from itertools import product
# # for i in product(data.schema_data()):
# #     print(i)
# for vals in product(*list(data.schema_data())):
#     print(vals)



# import json


# print(json.dumps(data))

# from jsonschema import validate
# schema = {
#      "type" : "object",
#      "properties" : {
#          "price" : {
#              "stock":{"type" : "number"}
#          },
#          "name" : {"type" : "string"},
#      },
#  }
# print(validate(instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema))

class FiledType:
    pass
    

dct = {"data" : {
    "name":FiledType(),
    "age":FiledType(),
    "hoby":[
                    {
                    "singing":{"rating":FiledType(),"how":FiledType()}},
               {
                   "dancing":{
                       "rating":FiledType(),"how":FiledType()
                   }
               } ],
    "others":{
        "dontknow":[],
        "dummydict":FiledType(),
        "newvariable":[FiledType(),3,4,{"somemoredict":FiledType()},5,6]
    }
    }}

    def verifydefinition(values):
        if isinstance(values,dict):
            for k,v in values.items():
                if isinstance(v,dict) and len(v) != 0:
                    verifydefinition(v)
                elif isinstance(v,list) and len(v) != 0:
                    verifydefinition(v)
                elif isinstance(v,FiledType):
                    pass
                else:
                    raise AttributeError(f"wrong datatype at {k} ,{v} ,use <class FieldType> ,cannot be empty dict() or str()")
        if isinstance(values,list):
            for i in values:
                if isinstance(i,dict) and len(i) != 0:
                    verifydefinition(i)
                elif isinstance(i,list) and len(i) != 0:
                    verifydefinition(i)
                elif isinstance(i,FiledType):
                    pass
                else:
                    raise AttributeError(f"wrong datatype at {i},use <class FieldType> ,cannot be empty dict() or str()")

for key,value in dct.get("data").items():
    # print(key,value)
    if isinstance(value,FiledType):
        pass
    elif isinstance(value,(dict,list)) and len(value) != 0:
        verifydefinition(value)
    else:
        raise AttributeError("schema not properly defined")
        