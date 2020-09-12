import pymongo

class Errors:

    class SchemaError(Exception):
        pass

    class DuplicateKeyErr(Exception):
        pass

class PrimaryKey:
    pass

class Optional:
    pass

##################################
# model library wrapping pymongo #
##################################

class DocumentModel(dict):
    """ Verifyes and saves the schema model.This class needs to be inherited and the schema should be a list.
        It gives a doccument styte verification
    Setup:- 
        exampleschema(Model):
            __schema__ = {
                "firstname" : [str,PrimaryKkey]  # Field parameter should be a list
                "middlename"  : [str,Optinal]
                "lastname" : [str]
                "age"  : [int]
            }
        exampleschema.connect()     # connect to collection 
        doc = excampleschema({"documents":"detalis"})
        doc.save()

    ##################
    Implemented methods:
    connect         - conenct to the database collection.
    insert          - Save the doccument
    findone         - find one doc from the collection 
    findal          - Find all doc if no specific key is provided
    update          - update one existing doc
    delete          - delete the doc provided 

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
        print(addtodoc)
        print(self)
        self.update(*addtodoc)
        print(self)
        if self.__connection__ == True:
            if self.__schema__ is not None:
                self.__verifySchema()
            try:
                collname = ".".join(self.__collname)
                print(self.__dbname, " ", collname)
                data = self.client[self.__dbname][collname].insert_one(self)
                self.__resetcounters()
                return data
            except pymongo.errors.DuplicateKeyError as e :
                self.__resetcounters()
                print(e)
                raise Errors.DuplicateKeyErr ("Doccument already present .Use update() instead")

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
                raise ValueError ("Incorrect filter object provided.should be Dict type")
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
    
    def __resetcounters(self):
        self.__counter *= 0
        self.__dbname *= 0
        self.__collname *= 0

    def __verifySchema(self,strictcheck=False):
        opt_count = 0
        for i in self.__schema__.items():
            # print(self.get(i[0]))
            # print(i)
            if self.get(i[0]) is not None:
                # print(tuple(i[1]))
                if isinstance(self.get(i[0]),tuple(i[1])):
                    if PrimaryKey in tuple(i[1]):
                        self.__createindex(i[0])
                        pass
                    # print(i , " verified")
                else:
                    raise Errors.SchemaError
            elif Optional in tuple(i[1]):
                opt_count +=1
            elif None in tuple(i[1]):
                continue
            else:
                raise Errors.SchemaError
        if len(self) != len(self.__schema__) - opt_count:
            raise Errors.SchemaError ("Schema didnot mathch")

    def __createindex(self,index_name):
        collection =  ".".join(self.__collname)
        # print(self.__dbname, " ", collection ," ", index_name )
        # print("I am here ==========================")
        self.client[self.__dbname][collection].create_index([(index_name,pymongo.ASCENDING)],unique=True)
    

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